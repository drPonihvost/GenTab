from flask import Blueprint, request, jsonify
from .models import Project
from .scripts import parser, upload_to_base
from flask_jwt_extended import get_jwt_identity, jwt_required

POSTS_PER_PAGE = 20

projects = Blueprint('projects', __name__)


@projects.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    # проверка корректности файла

    filename = request.files['file'].filename
    data = request.files.get('file').read().decode('utf-8')
    user_id = get_jwt_identity()
    data = parser(data=data, filename=filename)
    validation_data = data.get('validation_data')

    upload_to_base(data=data["project"], user_id=user_id, json=data["validation_data"])

    return jsonify(validation_data)


@projects.route('/projects/', methods=['GET', 'POST'])
@jwt_required()
def get_projects():
    page = request.args.get('page', 0, type=int)
    user_id = get_jwt_identity()
    project_query = request.args.get('name', type=str).strip()
    pagination_config = {'page': page, 'per_page': POSTS_PER_PAGE, 'error_out': False}
    pagination = Project.filter_user_projects(q=project_query, user_id=user_id).paginate(**pagination_config)

    return jsonify(
        {'project': [project for project in pagination.items],
         'total_items': pagination.total,
         'page': pagination.page,
         'page_size': pagination.per_page}
    )
