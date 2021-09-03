from flask import Blueprint, request, jsonify
from .models import Project, Object
from .scripts import parser, upload_to_base
from flask_jwt_extended import get_jwt_identity, jwt_required
from error import UnexpectedError
from sqlalchemy.orm.exc import UnmappedInstanceError
import traceback

POSTS_PER_PAGE = 20

projects = Blueprint('projects', __name__)


@projects.errorhandler(UnexpectedError)
def unexpected_error(e):
    errors = []
    errors.append(e.to_dict())
    return jsonify(errors), e.status_code


@projects.route('/validate', methods=['POST'])
@jwt_required()
def validate():
    # проверка корректности файла
    try:
        filename = request.files['file'].filename
        data = request.files.get('file').read().decode('utf-8')
        data = parser(data=data, filename=filename)
    except Exception as e:
        raise UnexpectedError(msg='Некорректный файл или формат данных', error=e)
    return jsonify(data)


@projects.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    user_id = get_jwt_identity()
    data = request.json
    try:
        msg = upload_to_base(data=data, user_id=user_id)
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

@projects.route('/delete_project', methods=['DELETE'])
@jwt_required()
def delete_project():
    user_id = get_jwt_identity()
    name = request.args.get('project')
    project = Project.get_by_user(
        name=name,
        user_id=user_id
    )
    try:
        Project.delete(project)
    except UnmappedInstanceError as e:
        raise UnexpectedError(msg=f'Ошибка при попытке удалить проект {name}', error=e)
    return jsonify({'msg': f'Проект {name} удален'})


@projects.route('/delete_object', methods=['DELETE'])
@jwt_required()
def delete_object():
    user_id = get_jwt_identity()
    project_name = request.args.get('project')
    object_name = request.args.get('object')
    project = Project.get_by_user(
        name=project_name,
        user_id=user_id
    )
    try:
        project_id = project.id
    except AttributeError as e:
        raise UnexpectedError(msg=f'Проект {project_name} не существует', error=e)
    sample = Object.get_by_name(
        name=object_name,
        project_id=project_id
    )
    try:
        Object.delete(sample)
    except UnmappedInstanceError as e:
        raise UnexpectedError(msg=f'Ошибка при попытке удалить объект {object_name}', error=e)
    return jsonify({'msg': f'Объект {object_name} удален'})
