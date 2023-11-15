from functools import partial
from typing import TYPE_CHECKING, Optional
import databases
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext

from src.users.models import get_users

if TYPE_CHECKING:
    from src.users.gql import UserType


class Context(BaseContext):
    """Context."""

    db: databases.Database

    def __init__(
        self,
        db: databases.Database,
        user_loader: DataLoader[int, Optional['UserType']],
    ):
        self.db = db
        self.user_loader = user_loader


def get_context(db: databases.Database) -> Context:
    return Context(
        db=db,
        user_loader=DataLoader(
            load_fn=partial(get_users, db),
        )
    )
