from flask import Flask, render_template, redirect, url_for,request,session
from flask_session import Session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from analysis import *
from models import *

import json
import chess

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db.init_app(app)


@app.route('/tutor')
def index():
    return render_template("index.html")

@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        p = get_player()

        if p.condition == 'control':
            session['count'] = 5
        else:
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
    sf_move, leela_next_move_for_player = sf_calc(fen, check)
    if leela_next_move_for_player:
        session['count'] =  session.get('count') + 1
    print('next move', leela_next_move_for_player)
    wrapped = [sf_move, leela_next_move_for_player]

    return json.dumps(wrapped)


def get_player():
    if ('player_id' not in session or
            Player.query.filter_by(id=session['player_id']).first() is None):
        
        username = str(hash(request.remote_addr)) # use the hash of IP address
        
        if Player.query.filter_by(username=username).count() > 0:
            player = Player.query.filter_by(username=username).first() # get the player with a username if existed
        else:
            # query the numer of people in each condition
            num_control = Player.query.filter_by(condition='control').count()
            num_test = Player.query.filter_by(condition='test').count()

            if num_test > num_control:
                condition = 'control'
            else:
                condition = 'test'
            player = Player(username=username, condition=condition)
            db.session.add(player)
            db.session.commit()
        session['player_id'] = player.id
    else:
        player = Player.query.filter_by(id=session['player_id']).first()
    return player


if __name__ == '__main__':
    app.run(debug=True)

    