import json
import os
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import config.db as db

app = FastAPI()

origins = ["*"]

app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow CORS
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
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")
    return messages

# WebSocket chat
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)  # convert the string data to JSON
            db.save_message(data['sender'], data['receiver'], data['message'])
            print(f"Message received from {data['sender']} to {data['receiver']}: {data['message']}")
            await manager.broadcast(data['message'])  # convert the JSON back to string before sending
    except WebSocketDisconnect:
        manager.disconnect(websocket)

