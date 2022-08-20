# tables/coupons.py
from datetime import datetime
from pickletools import stringnl_noescape

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base

# class User(Base):
#     __tablename__ = "users"

#     first_name = Column(String)
#     last_name = Column(String)
#     email = String(String)
#     created_at = Column(DateTime, index=True, default=datetime.utcnow)

class Test(Base):
    __tablename__ = "test"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
