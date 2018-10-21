# src/models/SetModel.py

from marshmallow import fields, Schema
import datetime

from . import db

class SetModel(db.Model):
    """
    Set Model
    """

    # table name
    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(75), nullable=False)
    status = db.Column(db.String(25), nullable=False)
    errors = db.Column(db.Text, nullable=False)
    sat_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # class constructor
    def __init__(self, data):
        """
        Class Constructor
        """
        self.sat_id = data.get('satellite_id')
        self.id = data.get('set_id')
        self.condtion = data.get('condition', '')
        self.status = data.get('status', '')
        self.errors = '|'.join(data.get('errors', ''))

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
    def get_all_sets():
        return SetModel.query.all()

    @staticmethod
    def get_one_set(id):
        return SetModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class SetSchema(Schema):
    id = fields.Int(dump_only=True)
    condition = fields.Str(required=True)
    status = fields.Str(required=True)
    errors = fields.Field(required=True)
    sat_id = fields.Int(required=True)

