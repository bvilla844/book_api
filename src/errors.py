from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from fastapi import FastAPI, status


class BookException(Exception):
    "This is the base class fo all book errors"

    pass


class InvalidToken(BookException):
    "User has provided an invalid or expired token"

    pass


class RevokedToken(BookException):
    "User has provided a token that has benn revoked"

    pass


class AccesTokenRequired(BookException):
    "User has provided a refresh token when an acces token is needed"

    pass


class RefreshTokenRequired(BookException):
    "User has provided a refreh token when an acces token is needed"

    pass


class InvalidCredentials(BookException):
    "User has provided wrong email or password"

    pass


class UserAlreadyExists(BookException):
    "User has provided an email for a user who exists during sign up"

    pass


class UserNotFound(BookException):
    "User has provided an user that does not exist"


class InsufficientPermission(BookException):
    "User does not have the neccessary permissopns to perfom an action"

    pass


class BookNotFound(BookException):
    "Book not found"

    pass

class AccountNotVerified(Exception):
    "Account not yet verified"

    pass

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exec: BookException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error code": "book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid email or password",
                "error code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Token is invalid or expired",
                "error code": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "error code": "token_revoked",
            },
        ),
    )

    app.add_exception_handler(
        AccesTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid acces token",
                "error code": "acces_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error code": "acces_token_required",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account not verified",
                "error code": "account_not_verified",
                "resolution":"Pleas check you email or credetial"
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    
        
