# coding: utf8
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from apptax.database import db

db = db
migrate = Migrate()

app_globals = {}


def init_app():
    if app_globals.get('app', False):
        app = app_globals['app']
    else:
        app = Flask(__name__)

    with app.app_context():
        app.config.from_pyfile('config.py')
        db.init_app(app)
        db.app = app
        app.config['DB'] = db
        migrate.init_app(app, db, directory='apptax/migrations')

        @app.teardown_request
        def _manage_transaction(exception):
            if exception:
                db.session.rollback()
            else:
                db.session.commit()
            db.session.remove()

        from pypnusershub import routes
        app.register_blueprint(routes.routes, url_prefix='/api/auth')

        from apptax.index import routes
        app.register_blueprint(routes, url_prefix='/')

        from apptax.taxonomie.routesbibnoms import adresses
        app.register_blueprint(adresses, url_prefix='/api/bibnoms')

        from apptax.taxonomie.routestaxref import adresses
        app.register_blueprint(adresses, url_prefix='/api/taxref')

        from apptax.taxonomie.routesbibattributs import adresses
        app.register_blueprint(adresses, url_prefix='/api/bibattributs')

        from apptax.taxonomie.routesbiblistes import adresses
        app.register_blueprint(adresses, url_prefix='/api/biblistes')

        from apptax.taxonomie.routestmedias import adresses
        app.register_blueprint(adresses, url_prefix='/api/tmedias')

        from apptax.taxonomie.routesbibtypesmedia import adresses
        app.register_blueprint(adresses, url_prefix='/api/bibtypesmedia')

        from apptax.utils.routesconfig import adresses
        app.register_blueprint(adresses, url_prefix='/api/config')


    return app


app = init_app()
CORS(app, supports_credentials=True)
if __name__ == '__main__':
    app.run()
