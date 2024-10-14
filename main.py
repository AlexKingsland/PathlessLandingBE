from flask import Flask, jsonify, request
from config import SecretsConfig
from database.models import db
from api import subscribe_activity
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(SecretsConfig)

def init_app():
    CORS(app, support_credentials=True) # Allow cross origin calls

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist

    # Register the API Blueprint
    app.register_blueprint(subscribe_activity.subscribe_bp)
    return app

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

if __name__ == '__main__':
    init_app()
    app.run(debug=True)