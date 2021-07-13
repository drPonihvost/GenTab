from base.base_models import BaseModel, db
from dataclasses import dataclass


@dataclass
class Project(BaseModel):
    name = db.Column(db.String(225))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    load_at = db.Column(db.DateTime)
    validation_data = db.Column(db.JSON)

    object = db.relationship('Object', backref='project', cascade='all,delete-orphan')

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}, user_id: {self.user_id}, load_at: {self.load_at}>'

    @classmethod
    def get_by_user(cls, name, user_id):
        return cls.query.filter_by(name=name, user_id=user_id).first()

    @classmethod
    def filter_by_user(cls, q, user_id):
        return cls.query.filter(cls.name.contains(q), cls.user_id == user_id)

    id: int
    name: str
    load_at: load_at
    validation_data: str
    object: 'Object'


@dataclass
class Object(BaseModel):
    __table_args__ = (db.UniqueConstraint('name', 'project_id'),)

    @classmethod
    def get_by_name(cls, name, project_id):
        return cls.query.filter_by(name=name, project_id=project_id).first()

    name = db.Column(db.String(50))
    project_id = db.Column(db.Integer,
                           db.ForeignKey('project.id'),
                           nullable=False)
    marker = db.relationship('Marker', backref='object', cascade='all,delete-orphan')

    id: int
    name: str
    marker: 'Marker'


@dataclass
class Marker(BaseModel):
    object_id = db.Column(db.Integer,
                          db.ForeignKey('object.id'),
                          nullable=False)
    name = db.Column(db.String(50))
    allele_1 = db.Column(db.String(5))
    allele_2 = db.Column(db.String(5))
    allele_3 = db.Column(db.String(5))
    allele_4 = db.Column(db.String(5))
    allele_5 = db.Column(db.String(5))
    allele_6 = db.Column(db.String(5))

    id: int
    name: str
    allele_1: str
    allele_2: str
    allele_3: str
    allele_4: str
    allele_5: str
    allele_6: str
