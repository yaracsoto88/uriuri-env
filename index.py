import json
import os
from typing import Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import config.db as db

app = FastAPI()

origins = ["*"]

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_index_html():
    html_file_path = os.path.join("static", "login/index.html")
    return FileResponse(html_file_path)

class LoginRequest(BaseModel):
    password: str
    email: str

@app.post("/login")
async def login(login_data: LoginRequest):
    email = login_data.email
    password = login_data.password
    if db.get_user(email, password) > 0:
        return {"message": "Login successful"}
    else:
        return {"message": "Login failed"}

class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str

@app.post("/register")
async def register(register_data: RegisterRequest):
    email = register_data.email
    username = register_data.username
    password = register_data.password
    if db.get_user(email, password) > 0:
        return {"message": "User already exists"}
    else:
        rows = db.create_user(email=email, username=username, password=password)
        if rows >= 1:
            return {"message": "User created"}
        else:
            return {"message": "Error creating user"}

class User(BaseModel):
    email: str

@app.post("/friends")
async def get_friends(user: User):
    data = db.get_friends(user.email)
    return data

class UserFriend(BaseModel):
    username: str

@app.post("/idfriend")
async def get_idfriend(user: UserFriend):
    data = db.get_idfriend(user.username)
    return data

@app.get("/mensajes")
async def get_messages_endpoint(emailUser: str = Query(...), idfriend: str = Query(...)):
    messages = db.get_messages(emailUser, idfriend)
    return messages

# WebSocket chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  

    async def connect(self, websocket: WebSocket, user_id: str):  
        await websocket.accept()
        self.active_connections[user_id] = websocket  

    def disconnect(self, user_id: str): 
        self.active_connections.pop(user_id, None)  

    async def send_message(self, message: str, receiver: str):  
        print(f"Sending message to {receiver}: {message}" )
        receiver_socket = self.active_connections.get(receiver)
        if receiver_socket:
            await receiver_socket.send_text(message)
            
manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    
    await manager.connect(websocket, db.get_idfriend_by_mail(user_id))
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)  
            db.save_message(data['sender'], data['receiver'], data['message'])
            print(f"Message received from {data['sender']} to {data['receiver']}: {data['message']}")
            try:
                await manager.send_message(data['message'], data['receiver'])
            except Exception as e:
                print(f"Error sending message: {e}")
                
    except WebSocketDisconnect:
        manager.disconnect(user_id) 

class Friend(BaseModel):
    email: str
    friend: str
    
@app.post("/addfriend")
async def add_friend(emails : Friend):
    print (emails)
    data = db.send_friend_request(emails.email, emails.friend)
    if data ==-1:
        return {"message": "Error al enviar la petición de amistad"}
    else:
        return {"message": "Petición de amistad solicitada"}
    
@app.post("/friend_request")
async def friend_requests(email: User):
    return db.get_friend_request(email.email)

class FriendRequest(BaseModel):
    email: str
    friend: str
    accept: bool
    
@app.post("/accept_friend")
async def accept_friend(friends: FriendRequest):
    if friends.accept:
        if db.accept_friend_request(friends.email, friends.friend)>=0:
            return {"message": "Amigo añadido correctamente"}
        else:
            return {"message": "Error al aceptar la petición"}
    else:
        if db.deny_friend_request(friends.email,friends.friend)>=0:
            return {"message": "Petición de amigo rechazada"}
        else:
            return {"message": "Error al rechazar la petición"}
    
@app.post("/get_name")
async def get_name(username: UserFriend):
    return db.get_name(username.username)


    