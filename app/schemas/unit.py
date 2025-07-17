from pydantic import BaseModel
from enum import Enum


class UnitSize(str, Enum):
    STUDIO = "STUDIO"
    ONE_BED = "1BR"
    TWO_BED = "2BR"
    THREE_BED = "3BR"


class ApartmentUnitBase(BaseModel):
    unit_number: str
    size: UnitSize
    rent: int
    property_id: int


class ApartmentUnitCreate(ApartmentUnitBase):
    pass


class ApartmentUnitRead(ApartmentUnitBase):
    id: int

    class Config:
        orm_mode = True
