import os
import requests

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users = []

@app.route("/")
def index():
    return render_template("login.html") 

@app.route("/chat")
def chat():
    return render_template("chat.html")

@socketio.on("message")
def transmit(data):
    message = data["message"]
    print(message)
    emit("transmit", {"message": message}, broadcast = True)