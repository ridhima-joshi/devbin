from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ── User ───────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    name: str
    email: str


# ── Paste ──────────────────────────────────────────────────────────────────────

class PasteCreate(BaseModel):
    name: str
    lang: str = "plaintext"
    code: str


class PasteOut(BaseModel):
    id: int
    name: str
    lang: str
    code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True