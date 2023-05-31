from flask import Flask, render_template, redirect, url_for,request

import json
import chess
from analysis import *

app = Flask(__name__)

@app.route('/tutor')
def index():
    return render_template("index.html")

@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        return render_template("index.html")

    return render_template("consent.html")

@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    sf_move, leela_next_move_for_player = sf_calc(fen)

    print('next move', leela_next_move_for_player)
    wrapped = [sf_move, leela_next_move_for_player]

    return json.dumps(wrapped)


if __name__ == '__main__':
    app.run(debug=True)

    