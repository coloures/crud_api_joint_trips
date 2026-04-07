from database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    user_id_pay = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    type_of_expense = Column(Integer, ForeignKey("expenseTypes.id"))
    description = Column(String, nullable=True)
    currency_id = Column(Integer, ForeignKey("currencies.id"))