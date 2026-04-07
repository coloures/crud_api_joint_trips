from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean)
    created_at = Column(Date, nullable=False)