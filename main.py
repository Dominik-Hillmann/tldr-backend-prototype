from fastapi import FastAPI

from app.api import api_router
# from app.core.config import settings

# app = FastAPI(title=settings.PROJECT_NAME)
app = FastAPI(title="my little stupid glued together PDF summarizer")

app.include_router(api_router, prefix="/api/v1")  # <-- add the api_router

@app.get("/")
async def hello_world():
    print("Works")
    return {"message": "Hello World"}