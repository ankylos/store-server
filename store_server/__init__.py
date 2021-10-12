from flask import Flask
from dotenv import load_dotenv()
load_dotenv()

def create_app():
    app = Flask(__name__)

    from store_server import routes
    app.register_blueprint(routes.main)

    return app
