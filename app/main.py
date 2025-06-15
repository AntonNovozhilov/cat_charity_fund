import uvicorn
from core.config import settings
from fastapi import FastAPI

from api.routers import main_router

app = FastAPI(title=settings.title)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
