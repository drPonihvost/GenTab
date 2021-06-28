from flask import Blueprint, request, jsonify
from .models import Project
from .file_loader import file_loader
from flask_jwt_extended import get_jwt_identity, jwt_required

POSTS_PER_PAGE = 20

POSTS_PER_PAGE = 20

projects = Blueprint('projects', __name__)


@projects.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    # проверка корректности файла

    filename = request.files['file'].filename
    data = request.files.get('file').read().decode('utf-8')
    user_id = get_jwt_identity()
    file_loader(filename, data, user_id)

    return jsonify(user_id)


@projects.route('/get_projects/', methods=['GET', 'POST'])
@jwt_required()
def get_projects():
    page = request.args.get('page', 0, type=int)
    user_id = get_jwt_identity()
    project_query = request.args.get('name', type=str).strip()
    pag_config = {'page': page, 'per_page': POSTS_PER_PAGE, 'error_out': False}
    pagination = Project.filter_by_name(q=project_query, user_id=user_id).paginate(**pag_config)

    return jsonify(
        {'project': [project for project in pagination.items]},
        {'total_items': pagination.total,
         'page': pagination.page,
         'page_size': pagination.per_page}
    )
