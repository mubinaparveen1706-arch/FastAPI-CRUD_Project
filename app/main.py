from fastapi import FastAPI

from app import models  # noqa: F401
from app.database import Base, engine
from app.routers import auth, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"status": "ok"}