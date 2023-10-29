from datetime import datetime as dt

from fastapi import Query
from pydantic import BaseModel
from pydantic.class_validators import List, Union
from schemas.users import UserModel
class RegisterPicnicModel(BaseModel):
    city_id: int
    datetime: dt


class PicnicModel(BaseModel):
    id: int
    city_id: int
    city_name: str
    time: dt
    users: List[UserModel]

    class Config:
        orm_mode = True


class PicnicReg(BaseModel):
    user_id: int
    picnic_id: int

class PicnicRegOutput(BaseModel):
    user: str
    picnic: int


class PicnicOutput(BaseModel):
    id: int
    city_id: int
    city_name: str
    time: dt
    users: Union[List[UserModel], list]

    class Config:
        orm_mode = True