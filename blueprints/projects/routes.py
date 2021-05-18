from flask import Blueprint, request, jsonify

from .file_loader import file_loader

projects = Blueprint('projects', __name__)


@projects.route('/upload', methods=['GET', 'POST'])
def upload():
    # проверка корректности файла

    filename = request.files['file'].filename
    data = request.files.get('file').read().decode('utf-8')
    file_loader(filename, data)

    return jsonify()
