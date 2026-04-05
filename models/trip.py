from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

class Trip(Base):
    __tablename__ = "trips"
    
    emoji = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    country = Column(String, nullable=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    currency_id = Column(Integer, nullable=False)
    budget = Column(Float, nullable=False)
    description = Column(String, nullable=True)