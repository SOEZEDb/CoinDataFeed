from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Coin(db.Model):
    __tablename__ = 'coinmarketcap'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.String)
    change_24h = db.Column(db.String)
    market_cap = db.Column(db.String)

    categories = db.relationship('Category', backref='coin', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    coin_id = db.Column(db.Integer, db.ForeignKey('coinmarketcap.id'))