from base.base_models import BaseModel
from datetime import timedelta
from base.data_base import db
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import NoResultFound


class UserError(Exception):
    pass


class PasswordError(Exception):
    pass


class Organization(BaseModel):
    name = db.Column(db.String())

    @classmethod
    def get_by_name(cls, org_name):
        try:
            org = cls.query.filter_by(name=org_name).one()
        except NoResultFound:
            return None
        return org


class User(BaseModel):
    password = db.Column(db.String())
    name = db.Column(db.String())
    surname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    organization_id = db.Column(db.Integer,
                                db.ForeignKey('organization.id'),
                                nullable=False)

    org = db.relationship('Organization', backref='user')

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
    def get_by_email(cls, email):
        try:
            user = cls.query.filter_by(email=email).one()
        except NoResultFound:
            return None
        return user

    @classmethod
    def authenticate(cls, email, password):
        user = cls.get_by_email(email=email)
        if not user:
            raise UserError

        if not bcrypt.verify(password, user.password):
            raise PasswordError
        return user


class Role(BaseModel):
    name = db.Column(db.String(), default='user')

    @classmethod
    def find_user_id(cls):
        role = cls.query.filter_by(name='user').one()
        return role.id


class UserRole(BaseModel):
    __table_name__ = 'user_role'
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    role_id = db.Column(db.Integer,
                        db.ForeignKey('role.id'),
                        nullable=False)

    user = db.relationship('User', backref='user_role')
    role = db.relationship('Role', backref='user_role')
