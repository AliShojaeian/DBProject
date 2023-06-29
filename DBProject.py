from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///messaging_system.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    isAdmin = Column(Boolean)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender = Column(String)
    receiver = Column(String)
    content = Column(String)
    date = Column(DateTime)
    isRead = Column(Boolean)


Base.metadata.create_all(engine)

def display_message(message):
    print(f"Sender: {message.sender}")
    print(f"Receiver: {message.receiver}")
    print(f"Content: {message.content}")
    print(f"Date: {message.date}")
    print(f"Is Read: {'Yes' if message.isRead else 'No'}")


def display_user(user):
    print(f"Username: {user.username}")
    print(f"Is Admin: {'Yes' if user.isAdmin else 'No'}")




        
