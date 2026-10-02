from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from .core.security import SecurityHelpers
from .deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: dict):
    password_hash = SecurityHelpers.hash_password(payload["password"])
    return {
        "message": "User created",
        "email": payload["email"],
        "password_hash": password_hash,
    }


@router.post("/login")
def login(payload: dict):
    if "email" not in payload or "password" not in payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email and password are required",
        )
    token = SecurityHelpers.create_token(payload["email"])
    return {"token": token, "token_type": "bearer"}


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {"user": current_user}


__all__ = ["router"]
