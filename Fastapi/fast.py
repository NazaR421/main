from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
USERS_FILE = "users.json"

def read_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    
def write_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users,f,indent=4)

@app.get("/",response_class=HTMLResponse)
async def read_root(request:Request):
    users = read_users()
    return templates.TemplateResponse("index.html",{"request":request,"users":users})

@app.post("/add_user")
async def add_user(login:str = Form(...), last_name: str=Form(...), first_name:str=Form(...), age: int=Form(...)):
    users = read_users()
    new_user = {"login":login, "last_name":last_name,"first_name":first_name,"age":age}
    users.append(new_user)
    write_users(users)
    return {"УВАГА!": f"Користувача '{login}' додано"}

@app.post("/delete_user")
async def delete_user(login: str = Form(...)):
    users = read_users()
    initial_len = len(users)
    users = [user for user in users if user["login"] != login]
    if len(users) < initial_len:
        write_users(users)
        return {"message": f"Користувача '{login}' видалено"}
    else:
        return {"message": f"Користувача з логіном '{login}' не знайдено"}
    
@app.get("/get_all_users", response_class=HTMLResponse)
async def get_all_users(request:Request):
    users_data = read_users()
    return templates.TemplateResponse("index.html",{"request":request,"users":users_data})

