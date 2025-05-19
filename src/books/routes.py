from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from .schemas import BookCreateModel, BookUpdate, Book, BookDetailModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleCherker
from src.errors import BookNotFound


book_router = APIRouter()
book_service = BookService()
acces_token_bearer = AccessTokenBearer()
role_checker = RoleCherker(["admin", "user"])


@book_router.get("/", response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_detail=Depends(acces_token_bearer),
    _:bool=Depends(role_checker)
) -> list:
    print(token_detail)
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/user/{user_uid}", response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_user_books_submissions(
    user_uid :str,
    session: AsyncSession = Depends(get_session),
    token_detail=Depends(acces_token_bearer),
    _:bool=Depends(role_checker)
) -> list:
    print(token_detail)
    books = await book_service.get_user_books(user_uid, session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[Depends(role_checker)])
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_detail=Depends(acces_token_bearer),
) -> dict:
    user_id = token_detail.get('user')['user_uid']
    new_book = await book_service.create_book(book_data,user_id, session)
    return new_book



@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[Depends(role_checker)])
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_detail=Depends(acces_token_bearer),
) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise BookNotFound()


@book_router.patch("/{book_uid}", response_model=Book, dependencies=[Depends(role_checker)])
async def update_book(
    book_uid: str,
    book_update_data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    token_detail=Depends(acces_token_bearer),
) -> Book:
    update_book = await book_service.update_book(book_uid, book_update_data, session)
    if update_book:
        return update_book
    raise BookNotFound()


@book_router.delete("/{book_uid}", status_code=status.HTTP_200_OK, dependencies=[Depends(role_checker)] )
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_detail=Depends(acces_token_bearer),
):
    book = await book_service.get_book(book_uid, session)
    if book:
        await book_service.delete_book(book_uid, session)
        return {"book": "deleted"}
    raise BookNotFound
