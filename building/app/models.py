from datetime import datetime

from . import db


class Building(db.Model):
    __tablename__ = 'building'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    year_construction = db.Column(db.Integer)

    bricks = db.relationship('Bricks', backref='bricks', uselist=False, lazy='joined')

    def __repr__(self):
        return f'<Building {self.address}>'


class Bricks(db.Model):
    __tablename__ = 'bricks'

    id = db.Column(db.Integer, db.ForeignKey('building.id'), primary_key=True)
    count_bricks = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Bricks {self.id}, count {self.count_bricks}>'
