import uvicorn
from fastapi import FastAPI

#from routes.admin_api import admin_router
from routes.users_api import user_router
from routes.prediction_api import prediction_router

app = FastAPI()

#app.include_router(admin_router, prefix="/admin")
app.include_router(user_router, prefix="/user")
app.include_router(prediction_router, prefix="/prediction")


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
