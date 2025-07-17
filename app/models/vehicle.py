from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    plate = Column(String, nullable=False)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)

    resident = relationship("Resident", back_populates="vehicles")
