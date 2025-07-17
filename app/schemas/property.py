from pydantic import BaseModel


class PropertyBase(BaseModel):
    name: str
    address: str
    unit_count: int


class PropertyCreate(PropertyBase):
    pass


class PropertyRead(PropertyBase):
    id: int

    class Config:
        orm_mode = True
