from fastapi import APIRouter

from api.endpoints import auth as api_auth
from endpoints import activities, events, auth, main, profile


api_router = APIRouter()

api_router.include_router(activities.router, prefix="/activity")
api_router.include_router(events.router, prefix="/event")
api_router.include_router(api_auth.router, prefix="/api/auth")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(main.router, prefix="")
api_router.include_router(profile.router, prefix="/user")

