from fastapi import APIRouter, Depends
from database.database import get_session
from typing import List
from services import User_Services, Transaction_Services, Prediction_Services
from model.schema import PydanticUsers, PydanticTransaction, PydanticPrediction

admin_route = APIRouter(tags=["Admin"])


@admin_route.get('/get_all_transactions', response_model=List[PydanticTransaction])
async def get_all_transactions(session=Depends(get_session)) -> list:
    return Transaction_Services.get_all_transactions(session)


@admin_route.get('/get_all_users', response_model=List[PydanticUsers])
async def get_all_users(session=Depends(get_session)) -> list:
    return User_Services.get_all_users(session)


@admin_route.get('/get_all_preds', response_model=List[PydanticPrediction])
async def get_all_preds(session=Depends(get_session)) -> list:
    return Prediction_Services.get_all_predictions(session)
