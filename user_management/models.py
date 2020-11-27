from . import db

# for test
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
