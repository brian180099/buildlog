from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.security import (
    SESSION_COOKIE_NAME,
    create_session_token,
    hash_password,
    session_cookie_options,
    verify_password,
)
from app.db.session import get_db
from app.models import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    MessageResponse,
    NicknameUpdateRequest,
    RegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(or_(User.email == payload.email, User.nickname == payload.nickname))
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 이메일 또는 닉네임입니다.",
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        nickname=payload.nickname,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 이메일 또는 닉네임입니다.",
        ) from error

    db.refresh(user)
    response.set_cookie(
        value=create_session_token(user.id),
        **session_cookie_options(),
    )
    return {"data": UserResponse.model_validate(user)}


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 맞지 않습니다.",
        )

    response.set_cookie(
        value=create_session_token(user.id),
        **session_cookie_options(),
    )
    return {"data": UserResponse.model_validate(user)}


@router.post("/logout", response_model=MessageResponse)
def logout(response: Response) -> dict[str, dict[str, str]]:
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    return {"data": {"message": "로그아웃되었습니다."}}


@router.get("/me", response_model=AuthResponse)
def me(current_user: User = Depends(get_current_user)):
    return {"data": UserResponse.model_validate(current_user)}


@router.patch("/me", response_model=AuthResponse)
def update_nickname(
    payload: NicknameUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_user = db.scalar(
        select(User).where(User.nickname == payload.nickname, User.id != current_user.id)
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 닉네임입니다.",
        )

    current_user.nickname = payload.nickname
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 닉네임입니다.",
        ) from error

    db.refresh(current_user)
    return {"data": UserResponse.model_validate(current_user)}

