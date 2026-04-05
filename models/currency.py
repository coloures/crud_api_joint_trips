from database import Base
from sqlalchemy import Column, Integer, String

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)