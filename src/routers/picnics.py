import datetime as dt

from fastapi import APIRouter, HTTPException, Query
from pydantic.class_validators import List

from database import City, Picnic, PicnicRegistration, Session, User
from schemas.picnics import (PicnicModel, PicnicOutput, RegisterPicnicModel,
                             PicnicReg, PicnicRegOutput)

picnics_router = APIRouter(prefix='/picnics')

pic_descr = 'Время пикника (по умолчанию не задано)'


@picnics_router.get('/get', summary='All Picnics',
                    tags=['picnic'],
                    response_model=List[PicnicOutput])
def all_picnics(datetime: dt.datetime = Query(default=None,
                                              description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True,
                                   description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    session = Session()
    picnics = session.query(Picnic)

    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    picnics = picnics.all()

    return [PicnicOutput.from_orm(picnic) for picnic in picnics]


@picnics_router.post('/create', summary='Picnic Add',
                     tags=['picnic'],
                     response_model=PicnicOutput)
def picnic_add(picnic: RegisterPicnicModel):
    """
    Добавление нового пикника
    """
    session = Session()
    # Существование города
    city = session.query(City).filter(City.id == picnic.city_id).first()
    if not city:
        raise HTTPException(status_code=400,
                            detail='Этого города не существует')

    # Некорректное время регистрации
    if picnic.datetime < dt.datetime.now():
        raise HTTPException(status_code=400,
                            detail='Некорректное время регистрации')

    picnic_object = Picnic(city_id=picnic.city_id, time=picnic.datetime)
    session.add(picnic_object)
    session.commit()
    return PicnicOutput.from_orm(picnic_object)


@picnics_router.post('/usersignup/',
                     summary='Picnic Registration',
                     tags=['picnic'],
                     response_model=PicnicRegOutput)
def register_to_picnic(data: PicnicReg):
    """
    Регистрация пользователя на пикник
    """
    session = Session()
    user = session.query(User).filter(User.id == data.user_id).first()

    # Если пользователь не существует
    if not user:
        raise HTTPException(status_code=400,
                            detail='Пользователя с этим id не существует')
    picnic = session.query(Picnic).filter(Picnic.id == data.picnic_id).first()

    # Если пикник не существует
    if not picnic:
        raise HTTPException(status_code=400,
                            detail='Пикника с этим id не существует')

    reg = PicnicReg(user_id=user.id, picnic_id=picnic.id)
    session.add(reg)
    session.commit()

    return {'user': f'{user.name} {user.surname}',
            'picnic': picnic.id}
