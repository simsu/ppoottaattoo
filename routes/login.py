import os
import json
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.crud.sns import create_sns
from database import SessionLocal



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def show_login_page(request: Request):
    load_dotenv()
    return templates.TemplateResponse(
        "login.html",
        {
            'request': request,
            'TWITCH_CLIENT_ID': os.environ.get('CLIENT_ID'),
        }
    )


@router.get("/redirect/twitch")
async def get_login_request(request: Request, code: str, scope: str, db: Session = Depends(get_db)):
    load_dotenv()
    data = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/token/twitch',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    twitch_request = requests.post(
        'https://id.twitch.tv/oauth2/token',
        data=data,
        headers=headers,
    )
    twitch_request_json = twitch_request.json()
    helix_header = {
        'Authorization': 'Bearer ' + twitch_request_json['access_token'],
        'Client-Id': client_id,
    }
    # 유저 email 불러와서 db에 저장하기.
    twitch_user_info = requests.get(
        'https://api.twitch.tv/helix/users',
        headers=helix_header
    )
    dict_twitch_user_info = twitch_user_info.json()
    json_twitch_user_info = json.dumps(dict_twitch_user_info)

    cs = create_sns(db, data=json_twitch_user_info)

    return cs
