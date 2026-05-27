from database import Base
from sqlalchemy import Column, Integer, String, Boolean, func, DateTime, ForeignKey


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))
    message = Column(String, nullable=False)
    remind_at = Column(DateTime(timezone=True), nullable=False)
    is_sent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
