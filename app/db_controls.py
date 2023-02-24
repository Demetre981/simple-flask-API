from app.db_model import User, engine
from sqlalchemy.orm import Session

session = Session(engine)


def add_new_item(item):
    session.add(item)
    session.commit()
    session.close()



def check_if_user_exists(nickname: str):
    user = session.query(User).where(User.nickname == nickname).first()
    return user