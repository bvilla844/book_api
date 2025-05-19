from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from src.config import Config
import jwt
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer


password_context = CryptContext(
    schemes=['bcrypt'],
    deprecated="auto"
)

serializer = URLSafeTimedSerializer(
        secret_key=Config.JWT_SECRET, 
        salt="email-configuration"
    )

ACCES_TOKEN_EXPIRY = 3600
REFRESH_TOKEN_EXPIRY = 2

def generate_paswd_hash(password: str) -> str:

    hash = password_context.hash(password)

    return hash

def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password,hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False)  -> str:
    payload = {
        'user': user_data,
        'exp': datetime.now(timezone.utc) + (expiry if expiry else timedelta(seconds=ACCES_TOKEN_EXPIRY)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }
    
    token = jwt.encode(
        payload= payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt= token,
            key= Config.JWT_SECRET,
            algorithms= [Config.JWT_ALGORITHM]
        )
        return token_data
    
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None
    
    
def create_url_safe_token(data:dict):

    token = serializer.dumps(data)

    return token

def decode_url_safe_token(token:str):
    try:
        token_data = serializer.loads(token)
        return token_data

    except Exception as e:
        logging.error(str(e))
