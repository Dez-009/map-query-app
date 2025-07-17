from pydantic import BaseModel


class VehicleBase(BaseModel):
    make: str
    model: str
    plate: str
    resident_id: int


class VehicleCreate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    id: int

    class Config:
        orm_mode = True
