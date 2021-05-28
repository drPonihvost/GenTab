from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__);

@auth.route('/token', methods=['POST'])
def get_token():
    json = request.get_json()
    
    if not json:
        return jsonify({ 'message': 'No auth data' }), 400
    
    username = json.get('username', None)
    password = json.get('password', None)
    
    if username != 'test' or password != 'test':
        return jsonify({ 'message': 'Bad username or password' }), 401

    access_token = create_access_token(identity=username)
    
    return jsonify(token=access_token)