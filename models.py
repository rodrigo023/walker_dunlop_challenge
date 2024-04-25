from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Preferences(Base):
    __tablename__ = "preferences"

    user_id = Column(Integer, primary_key=True)
    email_enabled = Column(Boolean, nullable=False, default=False)
    sms_enabled = Column(Boolean, nullable=False, default=False)

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
