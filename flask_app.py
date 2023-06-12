from flask import Flask, render_template, redirect, url_for,request,session
from flask_session import Session
import sqlite3
import json
import chess
from analysis import *


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connect = sqlite3.connect('database.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS PARTICIPANTS (name TEXT, \
    games INTEGER)')

@app.route('/tutor')
def index():
    return render_template("index.html")

@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        session['count'] = 0
        session['move'] = 0

        return render_template("index.html")

    return render_template("consent.html")

@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    print(session['count'],session['move'])
    session['move'] =  session.get('move') + 1
    if session.get('count') <= depth and session.get('move') > 5:
        check = True
    else:
        check = False
    print(session.get('count'),check)
    sf_move, leela_next_move_for_player = sf_calc(fen, check)
    if leela_next_move_for_player:
        session['count'] =  session.get('count') + 1
    print('next move', leela_next_move_for_player)
    wrapped = [sf_move, leela_next_move_for_player]

    return json.dumps(wrapped)

if __name__ == '__main__':
    app.run(debug=True)

    