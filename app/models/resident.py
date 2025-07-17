from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models import Base


class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    income = Column(Integer, nullable=True)
    occupation = Column(String, nullable=True)
    num_occupants = Column(Integer, nullable=False, default=1)
    unit_id = Column(Integer, ForeignKey("apartment_units.id"), nullable=False)

    unit = relationship("ApartmentUnit", back_populates="residents")
    payments = relationship("Payment", back_populates="resident")
    pets = relationship("Pet", back_populates="resident")
    vehicles = relationship("Vehicle", back_populates="resident")
    repairs = relationship("Repair", back_populates="resident")
