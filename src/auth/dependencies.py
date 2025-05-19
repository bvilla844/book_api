from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
from .utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import List, Any
from src.db.models import User
from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccesTokenRequired,
    InsufficientPermission,
    RevokedToken, 
    AccountNotVerified
)

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or not credentials.scheme.lower() == "bearer":
            raise InvalidToken()

        token = credentials.credentials

        try:
            token_data = decode_token(token)
        except ExpiredSignatureError:
            raise InvalidToken()
        
        except InvalidTokenError:
            raise InvalidToken()

        if await token_in_blocklist(token_data["jti"]):
            raise RevokedToken() or InvalidToken()
        
        self.verify_token_data(token_data)
        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh", False):
            raise AccesTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get("refresh", False):
            raise RefreshTokenRequired()


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user 


class RoleCherker:
    def __init__(self, allowed_roles:List[str]) ->None:

        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in self.allowed_roles:
            return True
        
        raise InsufficientPermission()


        