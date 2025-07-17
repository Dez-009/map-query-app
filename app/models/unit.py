from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.db.models import Base


class UnitSize(str, enum.Enum):
    STUDIO = "STUDIO"
    ONE_BED = "1BR"
    TWO_BED = "2BR"
    THREE_BED = "3BR"


class ApartmentUnit(Base):
    __tablename__ = "apartment_units"

    id = Column(Integer, primary_key=True)
    unit_number = Column(String, nullable=False)
    size = Column(Enum(UnitSize, name="unitsize"), nullable=False)
    rent = Column(Integer, nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)

    property = relationship("Property", back_populates="units")
    residents = relationship("Resident", back_populates="unit")
    repairs = relationship("Repair", back_populates="unit")
