from datetime import datetime
from base.base import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True)
    # user_id = 0
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Project {self.name}, created {self.created_at}, updated{self.updated_at}>'

