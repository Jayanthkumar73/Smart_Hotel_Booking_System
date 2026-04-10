# JWT (JSON Web Token) is used to securely identify a logged-in user
# Instead of asking password every time, we give the user a token after login
# That token is sent with every request to prove who they are

from jose import JWTError, jwt          # jose library handles creating and reading JWT tokens
from datetime import datetime, timedelta # datetime to set when the token expires
from fastapi import Depends, HTTPException, status  # for throwing errors if token is invalid
from fastapi.security import OAuth2PasswordBearer   # tells FastAPI "look for token in the request header"
from sqlalchemy.orm import Session      # to query the database
from database import get_db             # our DB session dependency from database.py
import models                           # to fetch User from DB using the ID inside the token


# ==================== SECRET CONFIG ====================

# This is the secret key used to SIGN the token
# Anyone with this key can create or read tokens — keep it secret, never share it
SECRET_KEY = "your_secret_key_here"

# The algorithm used to encode the token — HS256 is the most common standard
ALGORITHM = "HS256"

# How long the token stays valid — after 30 minutes the user must login again
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==================== OAUTH2 SCHEME ====================

# This tells FastAPI: "When a request comes in, look for a Bearer token in the Authorization header"
# The tokenUrl must point to an OAuth2-compatible token endpoint.
# Every protected route will use this to extract the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ==================== CREATE TOKEN FUNCTION ====================

def create_access_token(data: dict):
    # This function is called after a successful login to generate a JWT token
    # 'data' will be something like {"user_id": 5}

    to_encode = data.copy()            # Copy the data so we don't modify the original dict

    # Calculate the exact time when this token should expire
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiry time into the token data under the key "exp"
    # JWT standard uses "exp" to check if the token has expired
    to_encode.update({"exp": expire})

    # jwt.encode() converts the dictionary into an encoded JWT token string
    # It uses SECRET_KEY to sign it so nobody can tamper with it
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt                 # Return the token string — this is sent to the user after login


# ==================== GET CURRENT USER FUNCTION ====================

def get_current_user(
    token: str = Depends(oauth2_scheme),   # FastAPI automatically extracts the token from the request header
    db: Session = Depends(get_db)          # Get a DB session to fetch the user
):
    # This function is used in protected routes like /book-room
    # It reads the token, checks it's valid, and returns the logged-in user

    # Pre-define the error we'll throw if anything goes wrong with the token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,          # 401 = not authenticated
        detail="Could not validate credentials",           # Error message sent back
        headers={"WWW-Authenticate": "Bearer"},            # Standard header for token auth errors
    )

    try:
        # jwt.decode() reads and verifies the token
        # It checks: 1) was it signed with our SECRET_KEY? 2) has it expired?
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the user_id we stored inside the token when it was created
        # .get() returns None if "user_id" key doesn't exist in the token
        user_id: int = payload.get("user_id")

        # If there's no user_id in the token, it's invalid — raise the error
        if user_id is None:
            raise credentials_exception

    except JWTError:
        # JWTError is raised if the token is tampered with, expired, or malformed
        raise credentials_exception

    # Token is valid — now fetch the actual user from the database using the user_id
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    # If no user found with that ID (maybe user was deleted), raise the error
    if user is None:
        raise credentials_exception

    # Everything is fine — return the user object
    # The route that called get_current_user will receive this user directly
    return user