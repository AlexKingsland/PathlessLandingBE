from flask import Flask, jsonify, request
from config import SecretsConfig
from database.models import db
from api import subscribe_activity
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True) # Allow cross origin calls
app.config.from_object(SecretsConfig)
CORS(app, support_credentials=True) # Allow cross origin calls

db.init_app(app)

with app.app_context():
    db.create_all()  # Create the database tables if they don't exist

# Register the API Blueprint
app.register_blueprint(subscribe_activity.subscribe_bp)

if __name__ == '__main__':
    app.run(debug=True)