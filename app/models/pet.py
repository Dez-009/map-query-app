from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)

    resident = relationship("Resident", back_populates="pets")
