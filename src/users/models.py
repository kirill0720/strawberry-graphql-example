from typing import Optional
from databases import Database
import pydantic
from pypika.dialects import PostgreSQLQuery as Query, Table


class User(pydantic.BaseModel):
    id: int
    name: str


class CreateUserInput(pydantic.BaseModel):
    name: str


async def get_users(
    db: Database,
    ids: Optional[list[int]] = None,
) -> list[User]:
    users_tb = Table('users')
    query = Query.from_(users_tb).select(users_tb.star)

    if ids is not None:
        if not ids:
            return []
        query = query.where(
            users_tb.field('id').isin(ids),
        )

    return [
        User(**el._mapping)
        for el in await db.fetch_all(query=str(query))
    ]


async def create_user(
    db: Database,
    create_input: CreateUserInput,
) -> User:
    users_tb = Table('users')
    query = Query.into(users_tb).columns(
        tuple(create_input.model_dump().keys()),
    ).returning(users_tb.star)
    for value in create_input.model_dump().values():
        query = query.insert(value)
    row = await db.fetch_one(query=str(query))
    if not row:
        raise ValueError('empty row returned')
    return User(**row._mapping)
