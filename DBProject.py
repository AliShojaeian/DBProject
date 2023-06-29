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


class MessageController:
    def send_message(self, sender, receiver, content):
        date= datetime.now()
        isRead = False
        
        message = Message(sender=sender, receiver=receiver, content=content , date=date , isRead=isRead)
        session.add(message)
        session.commit()
        
    def mark_as_read(self,message):
        message.isRead = True
        session.commit()
class UserController:
    def create_user(self, username, password, is_admin):
        user = User(username=username, password=password, isAdmin=is_admin)
        session.add(user)
        session.commit()

    def login(self, username, password):
        user = session.query(User).filter_by(username=username, password=password).first()
        return user


message_controller = MessageController()
user_controller = UserController()

while True:
    print("=== Messaging System ===")
    print("1. Register")
    print("2. Login")
    print("3. Quit")
    choice = input("Enter your choice: ")
    if choice == "1":
        print("=== Register ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        is_admin = input("Is user an admin? (y/n): ").lower() == "y"
        user_controller.create_user(username, password, is_admin)
        print("Registration successful!")
    elif choice == "2":
        print("=== Login ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = user_controller.login(username, password)
        if user:
            print("Login successful!")
            


