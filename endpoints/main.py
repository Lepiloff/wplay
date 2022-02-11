from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from services.activities import ActivityService
from models.events import MembersQuantity


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/', response_class=HTMLResponse)
async def main_page(request: Request,
                    members: List = [e.value for e in MembersQuantity],
                    activity_service: ActivityService = Depends()):
    activity = await activity_service.get()
    return templates.TemplateResponse('base.html',
                                      context={
                                          'request': request,
                                          'members': members,
                                          'activities': activity
                                      }
                                      )

