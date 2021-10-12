from flask import Flask

def create_app():
    app = Flask(__name__)

    from store_server import routes
    app.register_blueprint(routes.main)

    return app
