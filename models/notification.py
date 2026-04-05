from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, Boolean

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean)
    created_at = Column(Date, nullable=False)