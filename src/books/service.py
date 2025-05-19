from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel,BookUpdate
from sqlmodel import select, desc
from src.db.models import Book
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_user_books(self, user_uid:str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid:str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data:BookCreateModel, user_uid:str, session: AsyncSession):

        book_data_dict = book_data.model_dump()
        published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d").date()

        new_book = Book(
            title=book_data_dict['title'],
            author=book_data_dict['author'],
            publisher=book_data_dict['publisher'],
            published_date=published_date,
            page_count=book_data_dict['page_count'],
            language=book_data_dict['language']
        )
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_uid:str, book_data:BookUpdate, session: AsyncSession):

        book_update = await self.get_book(book_uid,session)

        if book_update is not None:
            book_data_dict = book_data.model_dump(exclude_unset=True)
            for k, v in book_data_dict.items():
                setattr(book_update, k, v)
                
            book_update.updated_at = datetime.utcnow()
            await session.commit()
            await session.refresh(book_update)
            return book_update
        return None

    async def delete_book(self, book_uid:str, session: AsyncSession):
        book_delete = await self.get_book(book_uid,session)
        if book_delete is not None:
            await session.delete(book_delete)
            await session.commit()
        else:
            return None