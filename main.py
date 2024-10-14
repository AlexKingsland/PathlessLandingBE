from flask import Flask
from config import SecretsConfig
from database.models import db
from flask_cors import CORS
from api import subscribe_activity

app = Flask(__name__)
app.config.from_object(SecretsConfig)
CORS(app, support_credentials=True) # Allow cross origin calls

db.init_app(app)

with app.app_context():
    db.create_all()  # Create the database tables if they don't exist

# Register the API Blueprint
app.register_blueprint(subscribe_activity.subscribe_bp)

if __name__ == '__main__':
    app.run(debug=True)
