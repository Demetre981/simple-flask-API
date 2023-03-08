from database import session, User, Event
from db_controls import commit_new_item
from werkzeug.security import generate_password_hash

pwd = generate_password_hash("admin")
admin = User("admin", pwd, "admin@ad.com")
commit_new_item(admin)

event = session.query(Event).first()
print(event, "query")