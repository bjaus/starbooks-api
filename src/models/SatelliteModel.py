# src/models/SatelliteModel.py

from datetime import datetime
from marshmallow import fields, Schema

from . import db
from .SetModel import SetSchema

class SatelliteModel(db.Model):
    """
    Satellite Model
    """

    # table name
    __tablename__ = 'satellites'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    sets = db.relationship('SetModel', backref='satellites', lazy=True)

    # class constructor
    def __init__(self, data):
        """
        Class Constructor
        """
        self.id = data.get('satellite_id')
        timestamp = data.get('timestamp')
        if timestamp: timestamp = datetime.utcfromtimestamp(timestamp)
        else: timestamp = datetime.utcnow()
        self.timestamp = timestamp

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_satellites():
        return SatelliteModel.query.all()

    @staticmethod
    def get_one_satellite(id):
        return SatelliteModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class SatelliteSchema(Schema):
    """
    Satellite Schema
    """
    id = fields.Int(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)
    sets = fields.Nested(SetSchema, many=True)

