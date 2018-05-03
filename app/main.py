import os
from flask import Flask
import logging

from werkzeug.contrib.profiler import ProfilerMiddleware

import database
import cache



def create_app(config_filepath=None, import_name=None):

    if import_name is None:
        import_name = __name__
    app = Flask(__name__)
    setup_logging(app)

    app_settings= os.environ['APP_SETTINGS']
    if not app_settings:
        print("'APP_SETTINGS', not found in OS, setting default settings")
        app_settings = "DefaultConfig"

    app.config.from_object(app_settings)

    #app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="./profile_dir/")

    from api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint)

    cache.redis_store.init_app(app)
    database.db.init_app(app)

    return app


def setup_logging(app):
    from logging import Formatter
    root_logger = logging.getLogger()
    stream_logger = logging.StreamHandler()
    stream_logger.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stream_logger)
    logging.warn("Configured logging!")



if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=8081)

