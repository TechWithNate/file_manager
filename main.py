from fastapi import FastAPI
from routers import users, files
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(files.router)
