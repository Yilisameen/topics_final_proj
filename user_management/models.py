from . import db

class User(db.Model):
    """Data model for user accounts."""
    __tablename__ = 'useraccount'
    uid = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(30),
        index=False,
        unique=False,
        nullable=False
    )
    credibility = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    bio = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )
    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )
    suspend = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Watchlist(db.Model):
    """Data model for user watchlist."""
    __tablename__ = 'userwatchlist'
    recordid = db.Column(
        db.Integer,
        primary_key=True
    )
    uid = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    itemid = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    itemname = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    criteria = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<User {}, Item {}>'.format(self.uid, self.itemid)
