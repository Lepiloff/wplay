from datetime import datetime, time, date

from pydantic import BaseModel, StrictStr

from fastapi import Form

from .activity_schema import ActivityBase
from .location_schema import LocationBase
from models.events import Status


#TODO прочекать чтобы дата и время были не str а date time
class EventForm(BaseModel):
    street: str
    house: str
    title: str
    description: str
    activity: int
    is_private: bool
    start_date: date
    start_time: time

    @classmethod
    def as_form(cls, street: str = Form(...), house: str = Form(...),
                title: str = Form(...), description: str = Form(...),
                activity: str = Form(...), is_private: bool = Form(False),
                start_date: date = Form(...), start_time: time = Form(...)):
        return cls(
            street=street, house=house, title=title,
            description=description, activity=activity,
            is_private=is_private, start_date=start_date,
            start_time=start_time)


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
