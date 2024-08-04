import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import init_db
from routes.admin_api import admin_route
from routes.users_api import user_route
from routes.prediction_api import prediction_route
from services.logging_config import get_logger

logger = get_logger(logger_name=__name__)


app = FastAPI(logging=logger)
app.include_router(admin_route, prefix="/admin")
app.include_router(user_route, prefix="/user")
app.include_router(prediction_route, prefix="/prediction")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome!"}


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8080, reload=True)
