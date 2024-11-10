from flask import Flask
from flask_cors import CORS
from .db import db
from .config import Config
from .routes import track_bp  # Import routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure the app
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Register the blueprint for the routes
    app.register_blueprint(track_bp)

    return app

