from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

class TripMember(Base):
    __tablename__ = "tripMembers"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    role = Column(String, nullable=False)