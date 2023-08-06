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

def get_statistics_by_num_days(num_days):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=num_days - 1)

    session = create_session()
    dates = [start_date + datetime.timedelta(days=i) for i in range(num_days)]
    stats = []

    for date in dates:
        total_valid_time, total_invalid_time, statistic_date = session.query(
            func.sum(StatisticRecord.valid_time)/60,
            func.sum(StatisticRecord.invalid_time)/60,
            StatisticRecord.date_added
        ).filter(StatisticRecord.date_added == date).first()

        if total_valid_time is not None or  total_invalid_time is not None:
            stats.append((total_valid_time, total_invalid_time, statistic_date))

    session.close()
    return stats