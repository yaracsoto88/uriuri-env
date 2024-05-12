from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config.db import get_user
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
    html_file_path=os.path.join("static", "index.html")
    return FileResponse(html_file_path)

class LoginRequest(BaseModel):
    email: str
    password: str
@app.post("/login")
async def login(login_data: LoginRequest):
    email = login_data.email
    password = login_data.password
    print("llega quisskdsknadsjaskj")
    print(email, password)
    if get_user(email, password) > 0:
        return {"message": "Login successful"}
    else:
        return {"message": "Login failed"}