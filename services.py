from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password):
    return pwd_context.hash(password)

def check_password_hash(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)