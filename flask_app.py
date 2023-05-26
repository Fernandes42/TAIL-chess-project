from flask import Flask, render_template
import chess
from analysis import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    sf_move, next_move = sf_calc(fen)
    return sf_move


if __name__ == '__main__':
    app.run(debug=True)

    