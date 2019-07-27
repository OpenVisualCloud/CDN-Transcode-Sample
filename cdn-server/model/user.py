import datetime

from pymysql import Date
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from setting import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String(20))
    name = Column(String(30), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    mobile = Column(String(11),unique=True)
    email_addr = Column(String(30))
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    wx_openid = Column(String(50))
    qq_openid = Column(String(50))
    is_delete = Column(Boolean, nullable=False, server_default="0")

class Video(Base):
    __tablename__ = "video"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(20), nullable=False, unique=True)
    content = Column(String(255))
    addr = Column(String(100), nullable=False)
    img = Column(String(100))
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    is_delete = Column(Boolean, nullable=False, server_default="0")
    uid = Column(Integer,ForeignKey("user.id"), nullable=False)
    v2u = relationship("User", backref="u2v")
    duration = Column(Integer, nullable=False) 

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String(200), nullable=False)
    create_time = Column(DateTime, nullable=False, server_default=func.now())
    is_delete = Column(Boolean, nullable=False, server_default="0")
    uid = Column(Integer, ForeignKey("user.id"), nullable=False)
    c2u = relationship("User",backref="u2c")
    vid = Column(Integer, ForeignKey("video.id"), nullable=False)
    c2v = relationship("Video", backref="v2c")
