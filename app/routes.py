from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_login import current_user

from .forms import LoginForm
from .database import session
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from .db_controls import add_new_item, get_events_by
from .database import User, Event
from . import app, login_manager


def add_event_to_database(event_data):
    print(event_data)
    event_data["user"] = 1
    event = Event(**event_data)
    add_new_item(event)


def create_response(status_code):
    response = make_response()
    response.status_code = status_code
    return response


@app.route("/create_event", methods=["POST"])
def create_event():
    print(request)
    data_from_request = request.get_json()
    print(data_from_request)
    try:
        add_event_to_database(data_from_request)
        response = create_response(200)
    except Exception as e:
        print(e)
        response = create_response(500)

    return response


@app.route("/get_events_by_date/<date>", methods=["GET"])
def get_events_by_date(date):
    print(date[:10])
    data = get_events_by(date[:10])
    response = make_response(jsonify(data))
    return response


@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html")


@app.route("/test")
def test():
    import requests

    response = requests.get('https://www.boredapi.com/api/activity')
    print(response)
    if response.status_code == 200:
        data = response.json()["activity"]
    else:
        data = "ERROR"

    return render_template("main.html", data=data)



@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(405)
def handle_error(e):
    return render_template("custom_error.html", error=e.code)


@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":

        nickname = request.form["nickname"]
        email = request.form["email"]
        password = request.form["password"]

        user = session.query(User).where(User.nickname == nickname).first()
        print(user)

        if user:
            return redirect(url_for("signup"))

        new_user = User(nickname=nickname, email=email, password=generate_password_hash(password))
        print(new_user)
        session.add(new_user)
        session.commit()
        session.close()
    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login():
    data_from_request = request.get_json()

    name = data_from_request["nickname"]
    password = data_from_request["password"]

    user_check = session.query(User).where(User.nickname == name).first()

    if not user_check:
        print(name, password)
        response = make_response({"isLogged": False})
        return response

    if check_password_hash(user_check.password, password):
        print(name, password)
        response = make_response

@login_manager.user_loader
def load_user(user):
    return session.query(User).get(int(user))