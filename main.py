import os
from flask import Flask, session, render_template, redirect, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO
secret = os.environ['secret']

app = Flask(__name__)

io = SocketIO(app)


app.config.update(
    DEBUG = False,
    SECRET_KEY = secret,
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id

### CHAT HANDLING ###

@app.route('/')
@login_required
def chat():
    return render_template('chat.html', username=current_user.id)

@io.on('send')
def handle_message(json):
    data = {
        "message" : json["message"],
        "username" : current_user.id,
    }
    io.emit('broadcast', data, include_self=False)

### LOGIN/LOGOUT ###

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            user = User(username)
            login_user(user)
            return redirect('/')
        except Exception as error:
            return f"Error! Something bad happened during login!<br/>Error Details:</br><code>{error}</code>"
    elif request.method == 'GET':
        return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return "You are logged out. <a href='/login'>Login?</a>"


  
@login_manager.user_loader
def load_user(userid):
    return User(userid)
    

app.run('0.0.0.0', port=8081)


