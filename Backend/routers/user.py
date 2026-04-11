
# APIRouter lets us define routes in a separate file instead of putting everything in main.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Session is the database connection object we use to run queries
from sqlalchemy.orm import Session

# Our files
from database import get_db
import models
import schemas
from auth import create_access_token

from passlib.context import CryptContext

# ==================== SETUP ====================
router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# ==================== HELPER FUNCTIONS ====================
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ==================== REGISTER ====================
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed = hash_password(user.password)

    new_user = models.User(
        email=user.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==================== LOGIN ====================
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.LoginSchema, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 🔥 TEMP FIX: Support both hashed and plain passwords
    try:
        valid = verify_password(user.password, db_user.password)
    except:
        valid = (user.password == db_user.password)

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Optional: upgrade hash if needed
    try:
        if pwd_context.needs_update(db_user.password):
            db_user.password = hash_password(user.password)
            db.commit()
    except:
        pass  # skip if plain password

    access_token = create_access_token(data={"user_id": db_user.user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==================== TOKEN LOGIN ====================
@router.post("/token", response_model=schemas.Token)
def token_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 🔥 TEMP FIX: Support both hashed and plain passwords
    try:
        valid = verify_password(form_data.password, db_user.password)
    except:
        valid = (form_data.password == db_user.password)

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Optional: upgrade hash if needed
    try:
        if pwd_context.needs_update(db_user.password):
            db_user.password = hash_password(form_data.password)
            db.commit()
    except:
        pass

    access_token = create_access_token(data={"user_id": db_user.user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }