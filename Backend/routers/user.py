# APIRouter lets us define routes in a separate file instead of putting everything in main.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Session is the database connection object we use to run queries
from sqlalchemy.orm import Session

# Our files
from database import get_db          # Function that gives us a DB session
import models                        # SQLAlchemy User model (maps to users table)
import schemas                       # Pydantic schemas for input/output validation
from auth import create_access_token # Function to generate JWT token after login

# passlib is used to hash passwords securely before saving to DB
# CryptContext sets up the hashing algorithm.
from passlib.context import CryptContext
# ==================== SETUP ====================

# Creates a router object — all routes defined here will be grouped under this router
# prefix="/auth" means all routes here will start with /auth  e.g. /auth/register, /auth/login
# tags=["Auth"] groups these routes together in the auto-generated API docs at /docs
router = APIRouter(prefix="/auth", tags=["Auth"])

# Use Argon2 as the primary hasher.
# Keep bcrypt for backward compatibility so existing users can still log in.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# ==================== HELPER FUNCTIONS ====================
def hash_password(password: str):
    # Converts plain text password into a hashed string before saving to DB
    # e.g. "pass123" -> "$argon2id$v=19$m=..." (unreadable hash)
    # Even if DB is hacked, actual passwords are never exposed
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    # Compares the plain password the user typed with the hash stored in DB
    # Returns True if they match, False if they don't
    # We never "decode" the hash — passlib re-hashes and compares
    return pwd_context.verify(plain_password, hashed_password)


# ==================== REGISTER ROUTE ====================

@router.post("/register", response_model=schemas.UserResponse)
# @router.post means this route only accepts POST requests
# "/register" is the endpoint path → full path will be /auth/register
# response_model=schemas.UserResponse means FastAPI will format the response using UserResponse schema
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # user: schemas.UserCreate → FastAPI reads the request body and validates it using UserCreate schema
    # db: Session = Depends(get_db) → FastAPI automatically gives us a DB session

    # Step 1: Check if a user with this email already exists in the DB
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    # db.query(models.User) → SELECT * FROM users
    # .filter(models.User.email == user.email) → WHERE email = 'user@gmail.com'
    # .first() → gets the first match, or None if not found

    if existing_user:
        # If email already exists, stop and return 400 error
        # We don't want two accounts with the same email
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"   # This message is sent back in the response
        )

    # Step 2: Hash the password before saving — NEVER store plain text passwords
    hashed = hash_password(user.password)

    # Step 3: Create a new User object using the data from the request
    new_user = models.User(
        email=user.email,       # Email from the request body
        password=hashed         # Hashed password (not the plain one)
    )

    # Step 4: Add the new user to the DB session (staged, not saved yet)
    db.add(new_user)

    # Step 5: Commit saves the staged changes permanently to MySQL
    db.commit()

    # Step 6: Refresh gets the saved user back from DB including the auto-generated user_id
    db.refresh(new_user)

    # Step 7: Return the new user — FastAPI formats it using UserResponse schema
    # This means only user_id and email are returned, NOT the password
    return new_user


# ==================== LOGIN ROUTE ====================

@router.post("/login", response_model=schemas.Token)
# "/login" → full path will be /auth/login
# response_model=schemas.Token → response will contain access_token and token_type
def login(user: schemas.LoginSchema, db: Session = Depends(get_db)):
    # user: schemas.LoginSchema → expects email and password in request body

    # Step 1: Look for a user with the given email in the DB
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    # Step 2: If no user found with that email, return 404 error
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Step 3: Check if the password the user typed matches the hash in DB
    if not verify_password(user.password, db_user.password):
        # If passwords don't match, return 401 Unauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Optional migration: if stored hash is old/deprecated (e.g., bcrypt),
    # re-hash with Argon2 after successful login.
    if pwd_context.needs_update(db_user.password):
        db_user.password = hash_password(user.password)
        db.commit()

    # Step 4: Password is correct — generate a JWT token
    # We store user_id inside the token so we can identify the user later
    access_token = create_access_token(data={"user_id": db_user.user_id})

    # Step 5: Return the token — formatted using Token schema
    # Frontend will store this token and send it with every future request
    return {
        "access_token": access_token,
        "token_type": "bearer"          # "bearer" is the standard token type for JWT
    }


@router.post("/token", response_model=schemas.Token)
def token_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Swagger OAuth2 password flow sends 'username' and 'password' as form fields.
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    if pwd_context.needs_update(db_user.password):
        db_user.password = hash_password(form_data.password)
        db.commit()

    access_token = create_access_token(data={"user_id": db_user.user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }