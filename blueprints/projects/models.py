# from datetime import datetime
# from base.data_base import db
#
#
# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(225), unique=True)
#     # user_id = 0
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow())
#
#     def __init__(self, name):
#         self.name = name
#
#
#     def project_upload(self, commit=True):
#         project = Project.query.filter_by(name=self.name).first()
#         if project is None:
#             db.session.add(self)
#         else:
#             project.updated_at = datetime.utcnow()
#
#         if commit:
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 print("Ошибка загрузки")
#                 db.session.rollback()
#                 raise e
#         return project
#
#
#     def __repr__(self):
#         return f'<Project {self.id}>'
#
#
# class Object(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
#
#     def __init__(self, name, project_id):
#         self.name = name
#         self.project_id = project_id
#
#
#     def del_all_object(self):
#         g_object = Object.query.filter_by(name=self.name, project_id=self.project_id).all()
#         print(g_object)
#
#
#     def object_upload(self, commit=True):
#         g_object = Object.query.filter_by(name=self.name, project_id=self.project_id).first()
#         if g_object is None:
#             db.session.add(self)
#         else:
#             commit = False
#
#
#         if commit:
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 print("Ошибка загрузки")
#                 db.session.rollback()
#                 raise e
#         return g_object
#
#     def __repr__(self):
#         return f'<Object {self.name} id-{self.id} in project_id {self.project_id} >'
#
#
# class Marker(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     object_id = db.Column(db.Integer, db.ForeignKey('object.id'))
#     name = db.Column(db.String(50))
#     allele_1 = db.Column(db.String(5))
#     allele_2 = db.Column(db.String(5))
#     allele_3 = db.Column(db.String(5))
#     allele_4 = db.Column(db.String(5))
#     allele_5 = db.Column(db.String(5))
#     allele_6 = db.Column(db.String(5))
#
#     def __init__(self, name, object_id, allele_1=None, allele_2=None, allele_3=None,
#                  allele_4=None, allele_5=None, allele_6=None):
#         self.name = name
#         self.object_id = object_id
#         self.allele_1 = allele_1
#         self.allele_2 = allele_2
#         self.allele_3 = allele_3
#         self.allele_4 = allele_4
#         self.allele_5 = allele_5
#         self.allele_6 = allele_6
#
#     def __repr__(self):
#         return f'<Marker {self.name}>'


from datetime import datetime
from base.data_base import db

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


class Project(BaseModel):
    name = db.Column(db.String(225),
                     unique=True)
    # user_id = 0
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow())
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow())
    object = db.relationship('Object', backref='project')

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


    def before_save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()


    def before_update(self, *args, **kwargs):
        print('Calling Project models before_update')

    def after_update(self, *args, **kwargs):
        print('Calling Project models after_update')

class Object(BaseModel):
    __table_args__ = (db.UniqueConstraint('name', 'project_id'),)

    @classmethod
    def get_by_name(cls, name, project_id):
        return cls.query.filter_by(name=name, project_id=project_id).first()

    @classmethod
    def get_all_name(cls, project_id):
        return cls.query.filter_by(project_id=project_id).all()

    name = db.Column(db.String(50))
    project_id = db.Column(db.Integer,
                           db.ForeignKey('project.id'),
                           nullable=False)
    marker = db.relationship('Marker', backref='object', cascade='all,delete-orphan')

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
