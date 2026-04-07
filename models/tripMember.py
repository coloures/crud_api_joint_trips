from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

class TripMember(Base):
    __tablename__ = "tripMembers"
    
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    member_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, nullable=False)
    role = Column(String, nullable=False)