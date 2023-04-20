from fastapi import APIRouter

from app.api.endpoints import summarize  # <-- import the newly created endpoint

api_router = APIRouter()

api_router.include_router(summarize.router)  # <-- register the endpoint under /summarize prefix// WRONG ALREADY HAPPENS in @post
