from typing import Annotated, cast
import strawberry
from src.context import Context
from src.users.models import (
    CreateUserInput,
    User,
    create_user,
)
from strawberry.types import Info


@strawberry.experimental.pydantic.type(model=User, name='User')
class UserType():
    id: strawberry.auto
    name: strawberry.auto


@strawberry.type(name='Query', extend=True)
class UserQuery:

    @strawberry.field(name='user')
    async def user(
        self,
        info: Info[Context, None],
        id: int,
    ) -> UserType | None:
        return await info.context.user_loader.load(id)


@strawberry.experimental.pydantic.input(
    model=CreateUserInput, name='CreateUserInput',
)
class CreateUserInputType:
    name: strawberry.auto


@strawberry.type(name='Mutation', extend=True)
class UserMutation:

    @strawberry.mutation()
    async def create_user(
        self,
        info: Info[Context, None],
        create_input_gql: Annotated[
            CreateUserInputType,
            strawberry.argument(name='input'),
        ],
    ) -> UserType:
        create_input = create_input_gql.to_pydantic()
        return cast(
            UserType,
            await create_user(
                db=info.context.db,
                create_input=create_input,
            ),
        )
