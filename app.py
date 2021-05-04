import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from blueprints.auth.routes import auth
from blueprints.projects.routes import projects

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth)
app.register_blueprint(projects)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run()
