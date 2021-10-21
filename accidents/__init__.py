import os

from flask import Flask
from .dataproduct import dataproduct


def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder='./web/static',
                template_folder='./web/templates'
                #,static_url_path='/web/static'
                )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.auto_find_instance_path())
    except OSError:
        pass

    with app.app_context():
        pass

    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.register_blueprint(dataproduct.dtproductbp)
    return app