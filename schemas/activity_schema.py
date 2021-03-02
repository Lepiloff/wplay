from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str


class ActivityCreate(ActivityBase):
    pass


class ActivityList(ActivityBase):
    id: int
    is_active: bool



