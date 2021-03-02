from fastapi import APIRouter

from endpoints import activities, events


api_router = APIRouter()

api_router.include_router(activities.router, prefix="/activity")
api_router.include_router(events.router, prefix="/event")
