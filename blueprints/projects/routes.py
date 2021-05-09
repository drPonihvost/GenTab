from flask import Blueprint, request, jsonify, g, current_app
from .models import Project

projects = Blueprint('projects', __name__)

# db = None
# @projects.before_request
# def before_request():
#     """Установление соединения с БД"""
#     global db
#     db = current_app.config["sqlite:///base/gentab.db"]
#     print('Соединение установлено')
#
# @projects.teardown_request
# def teardown_request(request):
#     global db
#     db = None
#     return request

s = Project.query.filter_by(name='missing').first()
print(s is None)

@projects.route('/upload', methods=['GET', 'POST'])
def upload():


    # filename = request.files['file'].filename
    # data = request.files.get('file').read().decode('utf-8')
    #
    #
    # rows = data.splitlines()
    # keys = rows[0].split('\t')[:-1]
    # for row in rows[1:]:
    #     el = row.split('\t')[:-1]
    #     data = {}
    #     for index, key in enumerate(keys):
    #         data[key] = el[index]

    return jsonify()
