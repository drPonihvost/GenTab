from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#
# class Object(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
#     marker_id = db.Column(db.Integer, primary_key=True)
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return f'<Object {self.name}, in project_id {self.project_id} >'
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
#     def __init__(self, name, allele_1=None, allele_2=None, allele_3=None,
#                  allele_4=None, allele_5=None, allele_6=None):
#         self.name = name
#         self.allele_1 = allele_1
#         self.allele_2 = allele_2
#         self.allele_3 = allele_3
#         self.allele_4 = allele_4
#         self.allele_5 = allele_5
#         self.allele_6 = allele_6
#
#     def __repr__(self):
#         return f'<Marker {self.name}>'
