from flask import Blueprint, request
from .models import User, Roles, Organizations, UserRoles
from .schemas import Login, Registrations
from pydantic import ValidationError

auth = Blueprint('auth', __name__)


@auth.route('/token', methods=['POST'])
def get_token():
    try:
        params = Login(**request.json).dict()
    except ValidationError as e:
        return e.json(), 400
    else:
        user = User.authenticate(**params)

    token = user.get_token()
    return {"access_token": token}


@auth.route('/registrations', methods=['POST'])
def registrations():
    try:
        org_in_query = Registrations(**request.json).dict(include={'org_name'})
        params = Registrations(**request.json).dict(exclude={'org_name'})
    except ValidationError as e:
        return e.json(), 400

    org = Organizations.get_by_name(**org_in_query)
    if not org:
        org = Organizations(name=org_in_query['org_name'])
        org.save()
    user = User(organization_id=org.id, **params)
    user.save()
    role = Roles()
    role.save()
    user_role = UserRoles(user_id=user.id,
                          role_id=role.id)
    user_role.save()
    token = user.get_token()
    return {"access_token": token}
