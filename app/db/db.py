from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.statisticRecord import Base, StatisticRecord
from sqlalchemy import func
import datetime

def save_statistics_to_db(valid_time, invalid_time):
    session = create_session()

    new_object = StatisticRecord(valid_time=valid_time, invalid_time=invalid_time)
    session.add(new_object)
    session.commit()

    session.close()

def create_session():
    engine = create_engine('sqlite:///bonk.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_today_statistics():
        session = create_session()
        today = datetime.date.today()
        total_valid_time, total_invalid_time = session.query(
            func.sum(StatisticRecord.valid_time),
            func.sum(StatisticRecord.invalid_time)
        ).filter(StatisticRecord.date_added == today).first()

        session.close()

        if total_valid_time is None or total_invalid_time is None:
                return 0, 0
        else:
                return total_valid_time, total_invalid_time