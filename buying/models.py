from . import db

class Shoppingcart(db.Model):
    """Data model for user shopping cart."""
    __tablename__ = 'usercart'
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
    price = db.Column(
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

    def __repr__(self):
        return '<User {}, Item {}>'.format(self.uid, self.itemid)

class Shophistory(db.Model):
    """Data model for user shopping history."""
    __tablename__ = 'shophistory'
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
    price = db.Column(
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

    def __repr__(self):
        return '<User {}, Item {}>'.format(self.uid, self.itemid)