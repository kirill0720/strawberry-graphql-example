from typing import Optional
from databases import Database
import pydantic
from pypika.dialects import PostgreSQLQuery as Query, Table


class Book(pydantic.BaseModel):
    id: int
    title: str
    user_id: int


class CreateBookInput(pydantic.BaseModel):
    title: str
    user_id: int


async def get_books(
    db: Database,
    ids: Optional[list[int]] = None,
    after: str | None = None,
    first: int | None = None,
) -> list[Book]:
    books_tb = Table('books')
    query = Query.from_(books_tb).select(books_tb.star)

    if ids is not None:
        if not ids:
            return []
        query = query.where(
            books_tb.field('id').isin(ids),
        )
    if after:
        query = query.where(
            books_tb.field('id').gt(int(after)),
        )
    if first:
        query = query.limit(first)

    return [
        Book(**el._mapping)
        for el in await db.fetch_all(query=str(query))
    ]


async def create_book(
    db: Database,
    create_input: CreateBookInput,
) -> Book:
    books_tb = Table('books')
    query = Query.into(books_tb).columns(
        tuple(create_input.model_dump().keys()),
    ).returning(books_tb.star).insert(
        list(create_input.model_dump().values()),
    )
    row = await db.fetch_one(query=str(query))
    if not row:
        raise ValueError('empty row returned')
    return Book(**row._mapping)
