from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from crud import events


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# dont change method order
@router.get('/all')
async def _events():
    ev = await events.get_all()


@router.post('/all')
async def event_create(request: Request, street: str = Form(...), house: str = Form(...),
                                    activity: str = Form(...), title: str = Form(...),
                                    content: str = Form(...)):
    event = await events.post(street, house, title, content, activity)
    # return templates.TemplateResponse('events.html', context={'request': request, 'result': event})


@router.get('/{pk}')
async def event(request: Request, pk: int):
    event = await events.get(pk)
    # return templates.TemplateResponse('events.html', context={'request': request, 'result': event})


