from passlib.context import CryptContext

#  Used to handle password hashing and verification
# "bcrypt" is the hashing algorithm (note: spelling must be 'bcrypt', not 'bycrypt')
# 'deprecated="auto"' just means it will automatically mark old hashing schemes as outdated
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
