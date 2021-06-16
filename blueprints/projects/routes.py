from flask import Blueprint, request, jsonify
from .models import Project
from .file_loader import file_loader

POSTS_PER_PAGE = 20

projects = Blueprint('projects', __name__)


@projects.route('/upload', methods=['GET', 'POST'])
def upload():
    # проверка корректности файла

    filename = request.files['file'].filename
    data = request.files.get('file').read().decode('utf-8')

    file_loader(filename, data)

    return jsonify()


@projects.route('/return_projects/', methods=['GET', 'POST'])
def return_projects():
    page = request.args.get('page', 0, type=int)
    project_query = request.args.get('name', type=str).strip()
    pag_config = {'page': page, 'per_page': POSTS_PER_PAGE, 'error_out': False}
    pagination = Project.filter_by_name(q=project_query).paginate(**pag_config)
    projects_list = pagination.items

    return jsonify(
        {'project': [project for project in projects_list]},
        {'total_items': pagination.total,
         'page': pagination.page,
         'page_size': pagination.per_page}
    )
