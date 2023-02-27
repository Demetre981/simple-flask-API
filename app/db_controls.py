from flask import jsonify
from app.db_model import Event, User, engine
from sqlalchemy.orm import Session

session = Session(engine)


def add_new_item(item):
    session.add(item)
    session.commit()
    session.close()



def check_if_user_exists(nickname: str):
    user = session.query(User).where(User.nickname == nickname).first()
    return user


def get_events_by(date):
    events = session.query(Event).where(Event.date == date).all()
    response = jsonify({'events': [event.to_dict() for event in events]})
    return response