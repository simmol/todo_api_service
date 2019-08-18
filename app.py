from flask import Flask, jsonify


######################################
#### Application Factory Function ####
######################################

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.tasks import tasks_blueprint

    app.register_blueprint(tasks_blueprint)


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    register_blueprints(app)
    return app


app = create_app('flask.cfg')
