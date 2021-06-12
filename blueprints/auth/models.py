from base.base_models import BaseModel
from datetime import datetime, timedelta
from base.data_base import db
from dataclasses import dataclass
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token

class Organizations(BaseModel):
    name = db.Column(db.String())

    def __init__(self, *args, **kwargs):
        super(Organizations, self).__init__(*args, **kwargs)

class User(BaseModel):
    password = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    organization_id = db.Column(db.Integer,
                           db.ForeignKey('organizations.id'),
                           nullable=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id,
            expires_delta=expire_delta
        )
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user

class Roles(BaseModel):
    name = db.Column(db.String(), default='User')

    def __init__(self, *args, **kwargs):
        super(Roles, self).__init__(*args, **kwargs)

class UserRoles(BaseModel):
    __table_name__ = 'user_roles'
    user_id = db.Column(db.Integer,
                           db.ForeignKey('user.id'),
                           nullable=False)
    role_id = db.Column(db.Integer,
                           db.ForeignKey('user.id'),
                           nullable=False)