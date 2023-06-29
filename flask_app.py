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

last_move = [0,None]

with app.app_context():
    db.create_all()

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

def add_move(moves, cp, cpu, move_accepted):
    p = get_player()
    g = get_game(p)

    player_move = Move(game=g,
                       move_score=str(cp), raw_move=moves,
                       is_hint=cpu, uses_hint=move_accepted)

    db.session.add(player_move)
    db.session.commit()

@app.route('/move/<int:depth>/<path:fen>/<string:lastMove>')
def get_move(depth, fen,lastMove):
    session['move'] =  session.get('move') + 1
    if session.get('count') <= depth and session.get('move') > 5:
        check = True
    else:
        check = False
    sf_move, leela_next_move_for_player, cp = sf_calc(fen, check)
    if leela_next_move_for_player:
        session['count'] =  session.get('count') + 1
        last_move[0] = session['move']
        last_move[1] = leela_next_move_for_player
    wrapped = [sf_move, leela_next_move_for_player]

    move_seq = lastMove + "," + sf_move

    move_accepted = False


    if session['move'] == last_move[0] + 1:
        cpu = True
        if last_move[1] == last_move:
            move_accepted = True
    else:
        cpu = False
    add_move(move_seq,cp, cpu, move_accepted)

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

def get_game(player):
    if ('game_id' not in session or
            Game.query.filter_by(id=session['game_id'],
                                 player_won=None).first() is None):
        game = Game(player=player)
        
        db.session.add(game)
        db.session.commit()
        session['game_id'] = game.id
    else:
        game = Game.query.filter_by(id=session['game_id'],
                                    player_won=None).first()
    return game

if __name__ == '__main__':
    app.run(debug=True)

    