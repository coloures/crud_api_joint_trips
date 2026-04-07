from database import Base
from sqlalchemy import Column, Integer, ForeignKey

class TripBudgetCategory(Base):
    __tablename__ = "tripBudgetCategories"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    expense_type_id = Column(Integer, ForeignKey("expenseTypes.id"))
    planned_amount = Column(Integer, nullable=False)