import os
import requests

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room


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
    if request.method == "POST":
        channel = request.form.get("channel name")
        channels.append(channel)
    #return render_template("channel.html", users = users, channels = users[username].channels, username=username)
    return render_template("join.html", channels=channels, username=username)


@app.route("/newchannel/<string:username>", methods=["POST", "GET"])
def newchannel(username):
    print(username + " " + request.form.get("username"))
    return render_template("chat.html", person1 = username, person2 = request.form.get("username")) 

@app.route("/chat", methods=["POST"])
def chat():
    roomname = request.form.get("channelname")
    print(roomname)
    return render_template("chat.html", roomname = roomname)

@socketio.on("message")
def transmit(data):
    message = data["message"]
    roomname = data["room"]
    #roomname="first_room"
    print(message)
    print(roomname)
    join_room(roomname)
    emit("transmit", {"message": message, "roomname": roomname}, room=roomname)


