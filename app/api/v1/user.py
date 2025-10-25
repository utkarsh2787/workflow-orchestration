from fastapi import APIRouter, Depends, HTTPException, Response
import os
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import create_user, create_user_google, get_user_by_email, User
from app.schemas.user import UserCreate, UserGoogleCreate, UserLogin
from app.services.user import verify_password
from app.services.auth import create_user_token
from app.middleware.auth import get_current_user_from_cookie


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register")
def register_user(
    data: UserCreate, response: Response, session: Session = Depends(get_db)
):
    if get_user_by_email(session=session, email=data.email):
        raise HTTPException(status_code=400, detail="User already exists")

    usr = create_user(
        session=session,
        name=data.name,
        email=data.email,
        password=data.password,
    )

    token = create_user_token(usr.id, usr.email)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=18000,
    )

    return {
        "msg": "User registered successfully",
        "user": {"name": usr.name, "email": usr.email},
    }


@router.post("/login")
def login_user(data: UserLogin, response: Response, session: Session = Depends(get_db)):
    user = get_user_by_email(session=session, email=data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_user_token(user.id, user.email)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=18000,
    )

    return {
        "msg": "User logged in successfully",
        "user": {"name": user.name, "email": user.email},
    }


@router.post("/logout")
def logout_user(response: Response):
    # Delete cookie (path/domain should match how it was set).
    response.delete_cookie(key="access_token", path="/")
    return {"msg": "User logged out successfully"}



@router.post("/login/google")
def login_user_google(data:UserGoogleCreate,response: Response, session: Session = Depends(get_db)):
    
    user = get_user_by_email(session=session, email=data.email)
    if not user:
        user = create_user_google(
            session=session,
            name=data.name,
            email=data.email,
        )
    else:
        pass 
    response.set_cookie(
        key="access_token",
        value=create_user_token(user.id, user.email),
        httponly=False,
        secure=False,
        samesite="lax",
        max_age=18000,
    )
    return {"msg": "User logged in successfully"}


@router.get("/me")
def get_current_user(
    current_user: dict = Depends(get_current_user_from_cookie),
    session: Session = Depends(get_db),
):
    user = session.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        }
    }
