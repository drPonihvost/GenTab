from flask import Blueprint, request, jsonify

projects = Blueprint('projects', __name__);

@projects.route('/upload', methods=['POST'])
def upload():
    # Проверить, что файл корректный

    data = request.files.get('file').read().decode('utf-8');
    print(data);
    
    return jsonify()