from flask import Blueprint, request, jsonify
from .models import Project
from .scripts import parser, upload_to_base
from flask_jwt_extended import get_jwt_identity, jwt_required
from error import UnexpectedError

POSTS_PER_PAGE = 20

projects = Blueprint('projects', __name__)


@projects.errorhandler(UnexpectedError)
def unexpected_error(e):
    errors = []
    errors.append(e.to_dict())
    return jsonify(errors), e.status_code


@projects.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    # проверка корректности файла
    force_upload = request.args.get('force_upload')
    filename = request.files['file'].filename
    data = request.files.get('file').read().decode('utf-8')
    user_id = get_jwt_identity()
    try:
        data = parser(data=data, filename=filename)
    except Exception:
        raise UnexpectedError()
    validation_data = data.get('validation_data')

    try:
        upload_to_base(data=data, user_id=user_id)
    except Exception as e:
        raise UnexpectedError()

    if validation_data['status'] == 'invalid':
        return jsonify(validation_data), 400
    elif validation_data['status'] == 'partial_valid' and not force_upload:
        return jsonify(validation_data), 400
    else:
        return jsonify(validation_data), 200


@projects.route('/projects/', methods=['GET'])
@jwt_required()
def get_projects():
    page = request.args.get('page', 0, type=int)
    user_id = get_jwt_identity()
    project_query = request.args.get('name', type=str)
    if project_query and project_query.isalnum():
        project_query.strip()
    else:
        project_query = ''
    pagination_config = {'page': page, 'per_page': POSTS_PER_PAGE, 'error_out': False}
    pagination = Project.filter_by_user(q=project_query, user_id=user_id).paginate(**pagination_config)

    return jsonify(
        {'project': [project for project in pagination.items],
         'total_items': pagination.total,
         'page': pagination.page,
         'page_size': pagination.per_page}
    )
