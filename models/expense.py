from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, nullable=False)
    user_id_pay = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    type_of_expense = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    currency_id = Column(Integer, nullable=False)