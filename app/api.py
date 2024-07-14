import uvicorn
from fastapi import FastAPI
from database.database import init_db
from routes.admin_api import admin_route
from routes.users_api import user_route
from routes.prediction_api import prediction_route

app = FastAPI()
app.include_router(admin_route, prefix="/admin")
app.include_router(user_route, prefix="/user")
app.include_router(prediction_route, prefix="/prediction")


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
