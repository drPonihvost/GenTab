from datetime import datetime
from base.data_base import db
from dataclasses import dataclass

ALLELE_COUNT = 6


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    def before_save(self, *args, **kwargs):
        pass

    def after_save(self, *args, **kwargs):
        pass

    def save(self, commit=True):
        self.before_save()
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        self.after_save()

    def before_update(self, *args, **kwargs):
        pass

    def after_update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        db.session.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()


@dataclass
class Project(BaseModel):
    name = db.Column(db.String(225),
                     unique=True)
    # user_id = 0
    load_at = db.Column(db.DateTime,
                        default=datetime.utcnow())
    object = db.relationship('Object', backref='project', cascade='all,delete-orphan')

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def filter_on_request(cls, q):
        return cls.query.filter(Project.name.contains(q))

    id: int
    name: str
    load_at: load_at
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
