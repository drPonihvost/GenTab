from flask import Blueprint, request, jsonify, url_for
from .models import Project, Object, Marker
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

    return_projects = Project.query.all()

    page = request.args.get('page', 1, type=int)
    pagination = Project.query.paginate(page, per_page=POSTS_PER_PAGE, error_out=False)
    projects = pagination.items
    print(jsonify(return_projects))
    print(page)

    return jsonify({'project': [project for project in projects], 'total_items': pagination.total}, )

