from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import config.db as db

app = FastAPI()
origins = ["*"]

app.mount("/static", StaticFiles(directory="static"), name="static")

# allow cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_index_html():
    html_file_path=os.path.join("static", "login/index.html")
    return FileResponse(html_file_path)

class LoginRequest(BaseModel):
    password: str
    email: str
@app.post("/login")
async def login(login_data: LoginRequest):
    email = login_data.email
    password = login_data.password
    print(email, password)
    
    if db.get_user(email, password) > 0:
        return {"message": "Login successful"}
    else:
        return {"message": "Login failed"}


class ResgisterRequest(BaseModel):
    email: str
    password: str
    username: str
@app.post("/register")
async def register(login_data: ResgisterRequest):
    email=login_data.email
    username=login_data.username
    password=login_data.password
    
    if db.get_user(email, password) > 0:
        return {"message": "User already exists"}
    else:
        rows = db.create_user(email= email,username= username,password=password)
        print (rows)
        if (rows>=1):
            
            return {"message": "User created"}
        else:
            return {"message": "error al crear"}

class User(BaseModel):
    username: str

@app.get("/friends")
async def get_friends(username: User):
    return db.get_friends(username.username)