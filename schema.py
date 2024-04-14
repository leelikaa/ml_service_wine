from pydantic import BaseModel
from datetime import datetime



class UserCreate(BaseModel): #базовая информация при регистрации (думаю будет полезно при развитии сервиса)
    email: str
    password: str
    gender: str
    age: int
    city: str
    role: str #отделять обычных пользователей и админа
    

class UserGet(BaseModel, UserCreate):
    user_id: int
    balance: float
    
    class Config:
        orm_mode = True   


class Transaction(BaseModel):
    transaction_id: int
    user_id: int
    user: UserGet
    time: datetime.datetime   
    money: float
    type_: str #отделять пополнение/списание

    class Config:
        orm_mode = True   


class Model(BaseModel):
#здесь про модель, на основе которой будет прогноз, увязать с предсказанием


class Prediction(BaseModel):
    prediction_id: int
    user_id: int
    user: UserGet
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float
    result: float
    
    class Config:
        orm_mode = True

"""
class Result(BaseModel): #пока не очень понимаю надо ли создавать такой финализирующий всю работу класс 
    prediction_id: int
    user_id: int
    transaction_id: int
    
    class Config:
        orm_mode = True
"""