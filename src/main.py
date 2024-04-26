from fastapi import FastAPI

from .routers.preferences import main as preferences
from .routers.notifications import main as notifications
from . import models

from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(notifications.router)
app.include_router(preferences.router)
