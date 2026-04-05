from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

class TripBudgetCategory(Base):
    __tablename__ = "tripBudgetCategories"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False)
    expense_type_id = Column(Integer, nullable=False)
    planned_amount = Column(Integer, nullable=False)