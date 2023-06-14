import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType


db = SQLAlchemy()

class Player(db.Model):
    CONDITIONS = [
        ('control', 'control'),
        ('test', 'test')
    ]

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    games = db.relationship('Game', backref='player', lazy=True)
    condition = db.Column(ChoiceType(CONDITIONS))
    # TODO Number of games


    def __repr__(self):
        return '<Player: {}>'.format(self.username)


class Game(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          nullable=False)
    player_won = db.Column(db.Boolean, nullable=True)
    length = db.Column(db.Integer)
    hints = db.Column(db.Integer, default=0)
    moves = db.relationship('Move', backref='game', lazy=True)

    # do not need the opponent column until we have multiple opponents
    # opponent = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<Game: {} (player: {}, player won: {})>'.format(
            self.id, self.player_id, self.player_won)


class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_move = db.Column(db.Boolean, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    raw_move = db.Column(db.Text, nullable=True)
    is_hint = db.Column(db.Boolean, nullable=True)
    uses_hint = db.Column(db.Boolean, nullable=True)


    # Note sure we need this
    # move_number = db.Column(db.int, nullable=False)

    def __repr__(self):
        white = False
        if self.player_move and self.game.player_is_white:
            white = True
        if not self.player_move and not self.game.player_is_white:
            white = True
        return '<Move: {} (game={}, player={}, white={}, loc={}, score={})>'.format(
            self.id, self.game_id, self.player_move, white)