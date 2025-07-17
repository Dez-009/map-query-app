from pydantic import BaseModel


class ResidentBase(BaseModel):
    full_name: str
    email: str
    phone: str
    income: int | None = None
    occupation: str | None = None
    num_occupants: int
    unit_id: int


class ResidentCreate(ResidentBase):
    pass


class ResidentRead(ResidentBase):
    id: int

    class Config:
        orm_mode = True
