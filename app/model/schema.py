from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PydanticUsersData(BaseModel):  # базовая информация при регистрации (думаю будет полезно при развитии сервиса)
    #gender: str
    #age: int
    #city: str
    pass


class PydanticUsers(BaseModel):
    user_id: Optional[int] = None
    balance: float = 0.0
    email: str
    password: str
    role: Optional[str] = None # отделять обычных пользователей и админа

    class Config:
        orm_mode = True


class PydanticTransaction(BaseModel):
    transaction_id: int
    user_id: int
    user: PydanticUsers
    time: datetime
    money: float
    type_: str  # отделять пополнение/списание

    class Config:
        orm_mode = True


class PydanticWineDescription(BaseModel):
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


class PydanticPrediction(BaseModel):
    prediction_id: int
    user_id: int
    time: datetime
    wine_description: PydanticWineDescription
    result: float

    class Config:
        orm_mode = True

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data['wine_description'] = self.wine_description.dict()
        return data


'''
class PydanticPrediction(BaseModel):
    prediction_id: int
    user_id: int
    time: datetime
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
    result: float

    class Config:
        orm_mode = True
'''