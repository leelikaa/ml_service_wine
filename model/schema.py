from pydantic import BaseModel
from datetime import datetime


class UserData(BaseModel):  # базовая информация при регистрации (думаю будет полезно при развитии сервиса)
    #gender: str
    #age: int
    #city: str
    pass


class Users(BaseModel):
    user_id: int
    balance: float
    email: str
    telegram: str
    password: str
    role: str  # отделять обычных пользователей и админа

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    transaction_id: int
    user_id: int
    user: Users
    time: datetime
    money: float
    type_: str  # отделять пополнение/списание

    class Config:
        orm_mode = True


class WineDescription(BaseModel):
    fixed_acidity: float = 7.4
    volatile_acidity: float = 0.7
    citric_acid: float = 0.0
    residual_sugar: float = 1.9
    chlorides: float = 0.076
    free_sulfur_dioxide: float = 11.0
    total_sulfur_dioxide: float = 34.0
    density: float = 0.9978
    pH: float = 3.51
    sulphates: float = 0.56
    alcohol: float = 9.4


class Prediction(BaseModel, WineDescription):
    prediction_id: int
    user_id: int
    user: Users
    time: datetime
    result: float

    class Config:
        orm_mode = True
