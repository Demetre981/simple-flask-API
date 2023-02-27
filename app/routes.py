from app.db_controls import add_new_item, check_if_user_exists, get_events_by, session
from app.db_model import Event, User
from . import app, login_manager
from flask import flash, jsonify, make_response, redirect, render_template, request, url_for
from .forms import LoginForm, SignupForm
from flask_login import LoginManager, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash



@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    data_from_request["user"] = current_user.id
    event = Event(**data_from_request)
    add_new_item(event)
    response = make_response() 
    response.status_code = 200
    return response



@app.route("/get_events_by_date/<date>", methods=["GET"])
def get_events_by_date(date):
    return jsonify({"test": "test"}) 
    # return get_events_by(date)

@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html")


@app.route("/test")
def test():
    return str(current_user.is_authenticated)


@app.route("/login", methods=["POST", "GET"])
def login():
    formLo = LoginForm()
    if request.method == "POST":
        nickname = formLo.nickname.data
        password = formLo.password.data
        email = formLo.email.data


        user = check_if_user_exists(nickname)
        is_password_correct = False

        if user:
            is_password_correct = check_password_hash(user.password, password)

        if not user or not is_password_correct:
            flash("Try again and check your login details")
            return redirect(url_for("login"))

        login_user(user)
    #     return redirect("main")
    # return render_template("login.html")

        return redirect("main")
    
    return render_template("login.html", form=formLo)



@app.route("/signup", methods=["POST", "GET"])
def signup():
    formSi = SignupForm()
    if request.method == "POST":
        nickname = formSi.nickname.data
        password = generate_password_hash(formSi.password.data)
        email = formSi.email.data

        new_user = User(nickname=nickname, email=email, password=password)
        
        add_new_item(new_user)
        return redirect("/")
    return render_template("signup.html", form=formSi)




#     response = requests.get('https://www.boredapi.com/api/activity')

#     if response.status_code == 200:
#         data = response.json()["activity"]
#     else:
#         data = "ERROR"

#     return render_template("main.html", data=data)

@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(405)
def handle_error(e):
    return render_template("custom_error.html", error=e.code)


@login_manager.user_loader
def load_user(user_id: str):
    return session.query(User).where(User.id == user_id).first()