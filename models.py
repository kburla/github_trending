from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///mydatabase.db')

Base = declarative_base()

class DailyTrendingRepo(Base):
    __tablename__ = 'daily_trending_repos'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    forks = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return f"<DailyTrendingRepo(name='{self.name}', url='{self.url}', date='{self.date}')>"

class WeeklyTrendingRepo(Base):
    __tablename__ = 'weekly_trending_repos'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    forks = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return f"<WeeklyTrendingRepo(name='{self.name}', url='{self.url}', date='{self.date}')>"

class MonthlyTrendingRepo(Base):
    __tablename__ = 'monthly_trending_repos'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    language = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    forks = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return f"<MonthlyTrendingRepo(name='{self.name}', url='{self.url}', date='{self.date}')>"