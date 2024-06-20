from fastapi import FastAPI
from backend.routes import user

app = FastAPI()

app.include_router(user.router,prefix="/api")