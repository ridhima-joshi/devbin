from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import models, schemas, auth
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="devbin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ── DB dependency ──────────────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Auth helpers ───────────────────────────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = auth.verify_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── Auth routes ────────────────────────────────────────────────────────────────

@app.post("/register", response_model=schemas.TokenResponse)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        email=payload.email,
        name=payload.name,
        hashed_password=auth.hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth.create_token(user.email)
    return {"access_token": token, "token_type": "bearer", "name": user.name, "email": user.email}


@app.post("/login", response_model=schemas.TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if not user or not auth.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = auth.create_token(user.email)
    return {"access_token": token, "token_type": "bearer", "name": user.name, "email": user.email}


@app.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user


# ── Paste routes ───────────────────────────────────────────────────────────────

@app.get("/pastes", response_model=List[schemas.PasteOut])
def list_pastes(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Paste).filter(
        models.Paste.user_id == current_user.id
    ).order_by(models.Paste.created_at.desc()).all()


@app.post("/pastes", response_model=schemas.PasteOut, status_code=201)
def create_paste(payload: schemas.PasteCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    paste = models.Paste(**payload.dict(), user_id=current_user.id)
    db.add(paste)
    db.commit()
    db.refresh(paste)
    return paste


@app.put("/pastes/{paste_id}", response_model=schemas.PasteOut)
def update_paste(paste_id: int, payload: schemas.PasteCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    paste = db.query(models.Paste).filter(models.Paste.id == paste_id, models.Paste.user_id == current_user.id).first()
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found")
    for k, v in payload.dict().items():
        setattr(paste, k, v)
    paste.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(paste)
    return paste


@app.delete("/pastes/{paste_id}", status_code=204)
def delete_paste(paste_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    paste = db.query(models.Paste).filter(models.Paste.id == paste_id, models.Paste.user_id == current_user.id).first()
    if not paste:
        raise HTTPException(status_code=404, detail="Paste not found")
    db.delete(paste)
    db.commit()


@app.get("/health")
def health():
    return {"status": "ok"}