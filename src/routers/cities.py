from fastapi import APIRouter, Body, HTTPException, Query, Response
from pydantic.class_validators import List

from database import City, Session
from external_requests import CheckCityExisting
from schemas.cities import CityModel, CityOutput

cities_router = APIRouter(prefix='/cities')


@cities_router.post('/create', summary='Create City',
                    description='Создание города по его названию',
                    tags=['cities'],
                    response_model=CityOutput)
def create_city(city: CityModel):
    if city is None:
        raise HTTPException(status_code=400,
                            detail='Не указан параметр City')
    check = CheckCityExisting()
    if not check.check_existing(city.name):
        raise HTTPException(status_code=400,
                            detail='Город уже существует')

    city_object = Session().query(City).filter(
        City.name == city.name.capitalize()).first()

    if city_object:
        raise HTTPException(status_code=400,
                            detail='Такой город уже в базе')
    else:
        city_object = City(name=city.name.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id,
            'name': city_object.name,
            'weather': city_object.weather}


@cities_router.get('/get', summary='Get Cities',
                   tags=['cities'],
                   response_model=List[CityOutput])
def cities_list(q: str = Query(description="Название города", default=None)):
    """
    Получение списка городов
    """
    session = Session()
    # реализация поиска по городу
    if q:
        cities = session.query(City).filter(
            City.name.contains(q)).all()
    else:
        cities = session.query(City).all()

    return [{'id': city.id,
             'name': city.name,
             'weather': city.weather} for city in cities]