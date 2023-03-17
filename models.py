from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=False, default=1000)
    latest_rating_change = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    date_added = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())

    def __repr__(self):
        return self.name

    def num_games(self):
            return Result.query.filter((Result.player1_id == self.id) | (Result.player2_id == self.id)).count()



class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player1_score = db.Column(db.Integer, nullable=False)
    player2_score = db.Column(db.Integer, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    date_played = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())

    player1 = db.relationship('Player', foreign_keys=[player1_id])
    player2 = db.relationship('Player', foreign_keys=[player2_id])
    winner = db.relationship('Player', foreign_keys=[winner_id])

    def __repr__(self):
        return f'{self.player1.name} vs. {self.player2.name} ({self.player1_score} - {self.player2_score})'


class PlayerRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())

    player = db.relationship('Player', foreign_keys=[player_id])

