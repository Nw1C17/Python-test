from fastapi import APIRouter, Query
from pydantic.class_validators import List

from database import Session, User
from schemas.users import RegisterUserRequest, UserModel

users_router = APIRouter(prefix='/users')


@users_router.get('/get', summary='Список пользователей',
                  tags=['users'],
                  response_model=List[UserModel])
def users_list(min_age: int, max_age: int):
    """
    Список пользователей
    """
    session = Session()
    users = session.query(User).all()
    if min_age:
        users = session.query(User).filter(User.age >= min_age)
    if max_age:
        users = session.query(User).filter(User.age <= max_age)

    users = users.all()
    return [UserModel.from_orm(user) for user in users]


@users_router.post('/create', summary='CreateUser',
                   response_model=UserModel,
                   tags=['users'])
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)