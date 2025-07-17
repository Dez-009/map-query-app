from sqlalchemy import Column, Integer, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.db.models import Base


class PaymentStatus(str, enum.Enum):
    ON_TIME = "ON_TIME"
    LATE = "LATE"
    OUTSTANDING = "OUTSTANDING"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(PaymentStatus, name="paymentstatus"), nullable=False)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)

    resident = relationship("Resident", back_populates="payments")
