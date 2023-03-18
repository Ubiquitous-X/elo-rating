from datetime import datetime
from slugify import slugify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    wins = db.Column(db.Integer, nullable=False, default=0)
    losses = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=False, default=1000)
    latest_rating_change = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return self.name

    def generate_slug(self):
        self.slug = slugify(self.name)

    def win_ratio(self):
        if self.num_games() == 0:
            return 0
        return self.wins * 100 // self.num_games()

    def rank(self):
        players = Player.query.filter_by(is_active=True).order_by(Player.rating.desc()).all()
        return players.index(self) + 1

    def num_games(self):
        return Result.query.filter((Result.player1_id == self.id) | (Result.player2_id == self.id)).count()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


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

    def delete_and_update_players(self):
        db.session.delete(self)
        if self.winner == self.player1:
            self.player1.wins -= 1
            self.player2.losses -= 1
        else:
            self.player1.losses -= 1
            self.player2.wins -= 1
        db.session.commit()
        
    def __repr__(self):
        return f'{self.player1.name} vs. {self.player2.name} ({self.player1_score} - {self.player2_score})'


class PlayerRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())

    player = db.relationship('Player', foreign_keys=[player_id])

