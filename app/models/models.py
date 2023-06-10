from ..database import Base
from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, String, Boolean, Integer, text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,  nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, server_default='False')
    role = Column(String, server_default='user', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bucket_name = Column(String,  nullable=False)
    file_path = Column(String,  nullable=False)
    box = Column(String,  nullable=False)
    class_name = Column(String,  nullable=False)
    object_id = Column(Integer,  nullable=False)
    score = Column(Float ,  nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")