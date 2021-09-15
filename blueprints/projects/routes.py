from flask import Blueprint, request, jsonify, abort
from .models import Project, Object
from .scripts import parser, upload_to_base
from flask_jwt_extended import get_jwt_identity, jwt_required
from error import UnexpectedError, NotFound
import traceback

POSTS_PER_PAGE = 20

projects = Blueprint('projects', __name__)


@projects.errorhandler(UnexpectedError)
def unexpected_error(error):
    errors = []
    errors.append(error.to_dict())
    return jsonify(errors), error.status_code

@projects.errorhandler(NotFound)
def unexpected_error(error):
    errors = []
    errors.append(error.to_dict())
    return jsonify(errors), error.status_code

@projects.errorhandler(404)
def not_found(e):
    return jsonify({'msg': 'Not found'}), 404


@projects.route('/projects/', methods=['POST'])
@jwt_required()
def validate():
    # проверка корректности файла
    try:
        data = request.files.get('file').read().decode('utf-8')
        filename = request.files.get('file').filename
        data = parser(data=data, filename=filename)
    except Exception as e:
        raise UnexpectedError(msg='Некорректный файл или формат данных', error=e)
    return jsonify(data)


@projects.route('/projects/<string:project_name>', methods=['POST'])
@jwt_required()
def upload(project_name):
    user_id = get_jwt_identity()
    data = request.json
    if not data:
        raise NotFound(msg='Not found')
    try:
        msg = upload_to_base(data, user_id, project_name)
    except Exception as e:
        print(traceback.format_exc())
        raise UnexpectedError(msg='Ошибка загрузки', error=e)
    return jsonify(msg)


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

@projects.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    project = Project.get_by_id(project_id=project_id, user_id=user_id)
    if not project:
        raise NotFound(msg=f'Project not found')
    project.delete()
    return jsonify({'msg': f'success'})


@projects.route('/projects/<int:project_id>/objects/<int:object_id>', methods=['DELETE'])
@jwt_required()
def delete_object(project_id, object_id):
    user_id = get_jwt_identity()
    sample = Object.get_by_id(user_id=user_id, project_id=project_id, object_id=object_id)
    if not sample:
        raise NotFound(msg=f'Not found')
    sample = sample[2]
    sample.delete()
    return jsonify({'msg': f'success'})
