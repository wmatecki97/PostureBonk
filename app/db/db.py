from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.statisticRecord import Base, StatisticRecord

def save_statistics_to_db(valid_time, invalid_time):
    engine = create_engine('sqlite:///bonk.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    new_object = StatisticRecord(valid_time=valid_time, invalid_time=invalid_time)
    session.add(new_object)
    session.commit()

    session.close()