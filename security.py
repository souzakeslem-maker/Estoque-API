from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
TOKEN_ACCESS_EXPIRE_MINUTES = int(os.getenv("TOKEN_ACCESS_EXPIRE_MINUTES"))

argon2_content = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl='auth/login-form')