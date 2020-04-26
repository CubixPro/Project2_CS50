import os
import requests

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room
from flask_session import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["SESSION_PERMENENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = {} 
channels = []
messages = {}
class User:
    def __init__(self, name):
        self.status = 'logged in'
        self.channels = []
        self.messages = {}
        self.username = name 

@app.route("/")
def index():
    if session.get('username') != None:
        return render_template("join.html", channel=channels, username=session['username'])
    else:
        return render_template("login.html") 

@app.route("/enter", methods=["GET", "POST"])
def enter():
    print("Entered")
    username = request.form.get("username")
    session['username'] = username
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
    if messages.get(roomname) == None:
        messages[roomname] = {}
    return render_template("chat.html", roomname = roomname, username=session['username'], messages=messages[roomname])

@socketio.on("message")
def transmit(data):
    message = data["message"]
    roomname = data["room"]
    #roomname="first_room"
    #print(message)
    #print(roomname)
    #print(session['username'])
    print(messages[roomname])
    join_room(roomname)
    if messages.get(roomname) == None:
        messages[roomname] = [] 
    #messages[roomname].append(message)
    emit("transmit", {"message": message, "roomname": roomname, "username": session['username']}, room=roomname)


