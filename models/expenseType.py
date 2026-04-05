from database import Base
from sqlalchemy import Column, Integer, String

class ExpenseType(Base):
    __tablename__ = "expenseTypes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)