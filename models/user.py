from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    avatar = Column(String, nullable=True)