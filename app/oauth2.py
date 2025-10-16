from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET KEY
# Algorithm
# EXPIRATION TIME

SECRET_KEY = "X9dP3kL0sQaB7tVrU1nMhF8zYwE2jC6iO5pR4gTqN0xS8vW3aD9lK1mJ2bZ7cH5fG4oY6eP0rU9tV2iL8qN3sM1jA7wX5dF4zC6yR0bE9uT8pH2oG7nK3mJ1aD5vQ4lS6xW0fZ9iC8rL7gO2eP1tM3yN5wV4bU"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str =payload.get("user_id")

        if id is None:
            raise credentials_exception
        #may cause problem in the future the line below

        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
