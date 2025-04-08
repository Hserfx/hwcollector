from app.db.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship


class HotWheels(Base):
    __tablename__ = 'hot_wheels'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    toy_id = Column(Integer, unique=True, nullable=False)
    coll_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    series = Column(String(255), nullable=False)
    series_num = Column(String(50))
    img_url = Column(Text)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(50), primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    given_name = Column(String(100))
    picture = Column(Text)

class UserCollection(Base):
    __tablename__ = 'user_collection'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    hot_wheels_id = Column(Integer, ForeignKey('hot_wheels.id', ondelete='CASCADE'), nullable=False)
    date_added = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    user = relationship('User', backref='collection')
    hot_wheels = relationship('HotWheels', backref='owners')