from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from python_starter_project.user import UserDTO, UserFacade, UserId

from ..db import db_session
from ..ioc import Inject

router = APIRouter(prefix="/users")


class UserBase(BaseModel):
    name: str
    surname: str


class UserIn(UserBase):
    pass


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


@router.get(
    "/{id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "The user has not been found"}
    },
)
def get_user_by_id(
    id: UUID,
    user_facade: Annotated[UserFacade, Inject(UserFacade)],
) -> UserDTO:
    user = user_facade.get_by_id(UserId(id))

    return user


@router.get("/", response_model=list[UserOut], status_code=status.HTTP_200_OK)
def get_all_users(user_facade: Annotated[UserFacade, Inject(UserFacade)]) -> list[UserDTO]:
    users = user_facade.get_all()

    return users


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def add_new_user(
    payload: UserIn,
    user_facade: Annotated[UserFacade, Inject(UserFacade)],
    session: Annotated[Session, Depends(db_session)],
) -> UserDTO:
    new_user = user_facade.add(name=payload.name, surname=payload.surname)

    session.commit()

    return new_user
