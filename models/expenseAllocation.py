from database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Float

class ExpenseAllocation(Base):
    __tablename__ = "expenseAllocations"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    is_paid = Column("isPaid", Boolean, nullable=False)
