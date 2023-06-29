from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///messaging_system.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()



        
