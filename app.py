from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user
from forms import UserForm
from models import Users, Messages, Rooms
from flask_socketio import send, emit, join_room, leave_room, SocketIO
import json
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# DB configuration
app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb+srv://admin:admin@cluster0.zo5kc.mongodb.net/TecnicasAvanzadas?retryWrites=true&w=majority"
}

socketio = SocketIO(app)
db = MongoEngine(app)

# Login Manager configuration
login_manager = LoginManager()
login_manager.init_app(app)


# Initialization of the Secret Key
app.config['SECRET_KEY'] = 'very-complex-password'


@app.route('/chatroom', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('chatroom.html', username=current_user.username, salas=Rooms.objects)


@login_manager.user_loader
def load_user(id):
    return Users.objects(id=id).first()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    userForm = UserForm()

    if request.method == 'POST':
        if userForm.validate_on_submit():
            # Look for the first user with that username
            user = Users.objects(username=userForm.username.data, password=userForm.password.data).first()

            # If both passwords are the same you log in
            if userForm.password.data == user.password:
                login_user(user)

                return redirect(url_for('mostrar_salas'))

    return render_template('login.html', form=userForm)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    userForm = UserForm()

    if request.method == 'POST':
        if userForm.validate_on_submit():
            user = Users(username=userForm.username.data, password=userForm.password.data)
            app.logger.debug(f'New user added: {user}')
            # Add to the DB
            user.save()
            return redirect(url_for('log_in'))

    return render_template('signup.html', form=userForm)


@socketio.on("message")
def message(data):

    message_json = json.loads(data)
    print(message_json)
    # messageInfo = Messages(username=message_json["username"], data=message_json["data"])

    message = {
        "data": message_json["data"],
        "username": message_json["username"]
    }
    send(message, room=message_json["room"])


@socketio.on("join")
def join(data):

    data_json = json.loads(data)  # Convierte el JSON a un dict de Python
    join_room(data_json['room'])

    join_message = {
        "username": data_json["username"],
        "data": "HA ENTRADO A LA SALA"
    }

    emit("alerta", join_message, room=data_json["room"])


# @app.route("/salas", methods=["GET"])
# @login_required
# def mostrar_salas():

  #  return render_template("salas.html", salas=Rooms.objects, username=current_user.username)


if __name__ == '__main__':
    socketio.run(app)
