from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.models import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    unit_count = Column(Integer, nullable=False)

    units = relationship("ApartmentUnit", back_populates="property")
