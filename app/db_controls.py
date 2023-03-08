import json
from flask import jsonify
from .database import session, User, Event

def create_json_from(object):
    event_dict = object.__dict__

    # Видаляємо ключ "_sa_instance_state", який додає SQLAlchemy
    event_dict.pop('_sa_instance_state', None)

    #Перетворюємо дату та час на рядки, щоб повернути їх користувачу
    event_dict['time'] = event_dict['time'].strftime('%H:%M')
    event_dict['date'] = event_dict['date'].strftime('%Y-%m-%d')

    json_string = json.dumps(event_dict)
    return json_string


def commit_new_item(obj):
    session.add(obj)
    session.commit()


def check_if_user_exist(nickname: str):
    user = session.query(User).where(User.nickname == nickname).first
    return user


def get_events_by(date):
    events = session.query(Event).filter(Event.date == date, Event.user == user).all()
    jsonified_events = []
    for event in events:
        print(event)
        jsonified_events.append(create_json_from(event))
    return jsonified_events
