from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, DailyTrendingRepo, WeeklyTrendingRepo, MonthlyTrendingRepo

engine = create_engine('sqlite:///src/mydatabase.db')
Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)