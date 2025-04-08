from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from app.crud.users import create_user, get_user_by_email
import requests
from jose import jwt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

@router.get('/login/google')
async def login_google():
    google_auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&scope=openid%20profile%20email"
        "&access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)

@router.get('/auth/google')
async def auth_google(code: str, db: Session=Depends(get_db)):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")

    user_info_response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info_response.json()

    user = get_user_by_email(db, user_info["email"])
    if not user:
        user = create_user(db=db, user_data=user_info)

    payload = {
        "sub": user.email,
        "name": user.name,
        "picture": user_info.get("picture")
    }

    jwt_token = jwt.encode(payload, GOOGLE_CLIENT_SECRET, algorithm="HS256")
    return RedirectResponse(url=f'/v1?token={jwt_token}')

@router.get('/token')
async def get_token(token: str = Depends(oauth2_scheme)):
    return 