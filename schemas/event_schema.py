from datetime import datetime

from pydantic import BaseModel, StrictStr

from fastapi import Form

from .activity_schema import ActivityBase
from .location_schema import LocationBase
from models.events import Status


class EventForm(BaseModel):
    street: str
    house: str
    title: str
    content: str
    activity: int

    @classmethod
    def as_form(cls, street: str = Form(...), house: str = Form(...),
                title: str = Form(...), content: str = Form(...),
                activity: str = Form(...)):
        return cls(street=street, house=house, title=title, content=content, activity=activity)


class EventJoinForm(BaseModel):
    to_user_id: int

    @classmethod
    def as_form(cls, to_user_id: int = Form(...)):
        return cls(to_user_id=to_user_id)


class EventBase(BaseModel):
    id: int
    creator: int
    created_at: datetime
    title: str
    content: str
    status: Status
    is_active: bool
    is_group: bool
    is_private: bool
    location_id: LocationBase
    activities_id: ActivityBase

    class Config:
        orm_mode: True


class EventList(EventBase):
    pass


class EventSingle(EventBase):
    pass
