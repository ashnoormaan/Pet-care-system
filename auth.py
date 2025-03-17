import hashlib
import hmac
import jwt
import datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict

# Secret Key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔹 Hash Password
def hash_password(password: str) -> str:
    """ Hashes a password using SHA-256 """
    return hashlib.sha256(password.encode()).hexdigest()

# 🔹 Verify Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Compares plain and hashed passwords """
    return hmac.compare_digest(hash_password(plain_password), hashed_password)

# 🔹 Create JWT Token
def create_access_token(data: dict, expires_delta: int = 60):
    """Creates a JWT token with expiration time."""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})

    # ✅ Ensure `sub` (user ID) is an integer when decoding
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])  # Store as string

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# 🔹 Verify JWT Token
def verify_access_token(token: str = Depends(oauth2_scheme)):
    """Verifies JWT token and returns payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # ✅ Ensure `sub` (user_id) is returned as a string
        if "sub" in payload:
            payload["sub"] = str(payload["sub"])  

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    