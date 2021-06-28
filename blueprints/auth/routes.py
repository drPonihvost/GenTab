from flask import Blueprint, request, jsonify
from .models import User, Roles, Organizations, UserRoles

auth = Blueprint('auth', __name__)


@auth.route('/token', methods=['POST'])
def get_token():
    params = request.json
    user = User.authenticate(email=params.get('username'),
                             password=params.get('password'))
    if not user:
        return jsonify({'message': 'No auth data'}), 400
    token = user.get_token()
    return {"token": token}

@auth.route('/registrations', methods=['POST'])
def registrations():
    params = request.json
    org = Organizations(name=params.get('org_name'))
    org.save()
    user = User(email=params.get('email'),
                password=params.get('password'),
                name=params.get('name'),
                surname=params.get('surname'),
                organization_id=org.id)
    user.save()
    role = Roles()
    role.save()
    user_role = UserRoles(user_id=user.id,
                          role_id=role.id)
    user_role.save()
    token = user.get_token()
    return {"access_token": token}
