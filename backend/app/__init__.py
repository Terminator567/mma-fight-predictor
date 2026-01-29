from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}}
    )
    
    from .routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app
