from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.models import Base


class RepairStatus(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Repair(Base):
    __tablename__ = "repairs"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    status = Column(Enum(RepairStatus, name="repairstatus"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    unit_id = Column(Integer, ForeignKey("apartment_units.id"), nullable=False)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=True)

    unit = relationship("ApartmentUnit", back_populates="repairs")
    resident = relationship("Resident", back_populates="repairs")
