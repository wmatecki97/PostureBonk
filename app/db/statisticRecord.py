from sqlalchemy import Date, create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
import datetime

Base = declarative_base()

class StatisticRecord(Base):
    __tablename__ = 'sitting_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valid_time = Column(Integer)
    invalid_time = Column(Integer)
    date_added = Column(Date)

    def __init__(self, valid_time, invalid_time):
        self.valid_time = valid_time
        self.invalid_time = invalid_time
        self.date_added = datetime.date.today()