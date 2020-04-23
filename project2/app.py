import os
import requests

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users = {} 
messages = []
channels = []
class User:
    def __init__(self, name):
        self.status = 'logged in'
        self.channels = []
        self.messages = {}
        self.username = name 

@app.route("/")
def index():
    return render_template("login.html") 

@app.route("/enter", methods=["GET", "POST"])
def enter():
    print("Entered")
    username = request.form.get("username")
    if users.get(username) == None :
        p =  User(username)
        users[username] = p 

    return render_template("channel.html", users = users, channels = users[username].channels)

@app.route("/chat")
def chat():
    return render_template("chat.html")

@socketio.on("message")
def transmit(data):
    message = data["message"]
    print(message)
    emit("transmit", {"message": message}, broadcast = True)


