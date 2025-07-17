from pydantic import BaseModel
from enum import Enum
from datetime import date


class PaymentStatus(str, Enum):
    ON_TIME = "ON_TIME"
    LATE = "LATE"
    OUTSTANDING = "OUTSTANDING"


class PaymentBase(BaseModel):
    amount: float
    date: date
    status: PaymentStatus
    resident_id: int


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int

    class Config:
        orm_mode = True
