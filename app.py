import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from blueprints.auth.routes import auth
from blueprints.projects.routes import projects
from base.data_base import db


def create_app(test=False):
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(auth)
    app.register_blueprint(projects)

    # config
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PROJECT_DATA_BASE')
    if test:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_PROJECT_DATA_BASE')
        print("Создана тестовая база")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt = JWTManager(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
