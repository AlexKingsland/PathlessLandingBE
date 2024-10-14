from flask import Flask
from config import SecretsConfig
from database.models import db
from api import subscribe_activity
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(SecretsConfig)

    CORS(app, support_credentials=True) # Allow cross origin calls

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist

    # Register the API Blueprint
    app.register_blueprint(subscribe_activity.subscribe_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)