from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class RepairStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class RepairBase(BaseModel):
    description: str
    status: RepairStatus
    unit_id: int
    resident_id: int | None = None


class RepairCreate(RepairBase):
    pass


class RepairRead(RepairBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
