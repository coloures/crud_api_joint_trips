from database import Base
from sqlalchemy import Column, Integer, Boolean

class ExpenseAllocation(Base):
    __tablename__ = "expenseAllocations"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    isPaid = Column(Boolean, nullable=False)