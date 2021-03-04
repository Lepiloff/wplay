from pydantic import BaseModel


class LocationBase(BaseModel):
    id: int
    city: str
    street: str
    building: str





