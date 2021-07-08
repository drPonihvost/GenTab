from flask import Blueprint, request, jsonify
from .models import User, Roles, Organizations, UserRoles
from .schemas import Login, Registrations
from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound

auth = Blueprint('auth', __name__)


@auth.route('/token', methods=['POST'])
def get_token():
    try:
        params = Login(**request.json).dict()
        user = User.authenticate(**params)
    except ValidationError as e:
        return e.json(), 400

    token = user.get_token()
    return {"access_token": token}

@auth.route('/registrations', methods=['POST'])
def registrations():
    try:
        params = Registrations(**request.json).dict()
    except ValidationError as e:
        return e.json(), 400

    org = Organizations(name=params.org_name)
    org.save()
    user = User(**params)
    user.save()
    role = Roles()
    role.save()
    user_role = UserRoles(user_id=user.id,
                          role_id=role.id)
    user_role.save()
    token = user.get_token()
    return {"access_token": token}
