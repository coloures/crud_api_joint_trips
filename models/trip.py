from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

class Trip(Base):
    __tablename__ = "trips"
    
    emoji = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    country = Column(String, nullable=False)
    start_date = Column("startDate", Date, nullable=False)
    end_date = Column("endDate", Date, nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    budget = Column(Float, nullable=False)
    description = Column(String, nullable=True)
