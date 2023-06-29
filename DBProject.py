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
            while True:
                print("=== User Menu ===")
                print("1. Send Message")
                if user.isAdmin:
                    print("2. Send Message to All Users")
                    print("3. View All Messages")
                    print("4. Logout")
                else:
                    print("2. New Messages")
                    print("3. Logout")
                user_choice = input("Enter your choice: ")
                if user_choice == "1":
                    sender = user.username
                    receiver = input("Enter receiver's username: ")
                    content = input("Enter message content: ")
                    message_controller.send_message(sender, receiver, content)
                    print("Message sent successfully!")
                elif user_choice == "2":
                    if user.isAdmin:
                        content = input("Enter message content: ")
                        all_users = session.query(User).all()
                        for u in all_users:
                            if u.username != user.username:
                                message_controller.send_message(user.username, u.username, content)
                        print("Message sent to all users!")
                    else:
                        print("=== Your Messages ===")
                        messages = session.query(Message).filter_by(receiver=user.username, isRead=False).all()
                        if messages:
                            for i, message in enumerate(messages):
                                print(f"Message {i + 1}:")
                                display_message(message)
                                print()

                            message_choice = input("Enter the message number to mark as read (0 to cancel): ")
                            if message_choice.isdigit():
                                message_choice = int(message_choice)
                                if 1 <= message_choice <= len(messages):
                                    message = messages[message_choice - 1]
                                    message_controller.mark_as_read(message)
                                    print("Message marked as read.")
                                elif message_choice != 0:
                                    print("Invalid message number.")
                        else:
                            print("No unread messages.")

                


