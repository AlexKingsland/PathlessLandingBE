import re
from flask import Flask, jsonify, request
from config import SecretsConfig, ValidationConfig
from database.models import Subscriber, db
from api import subscribe_activity
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(SecretsConfig)
CORS(app, support_credentials=True) # Allow cross origin calls

db.init_app(app)

with app.app_context():
    db.create_all()  # Create the database tables if they don't exist

# Regex pattern for email validation
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()

    # Validate input
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    
    name = data['name']
    email = data['email']

    if len(name) > ValidationConfig.MAX_NAME_LEN:
        return jsonify({'error': 'Name too long'}), 400
    elif len(email) > ValidationConfig.MAX_EMAIL_LEN:
        return jsonify({'error': 'Email too long'}), 400

    # Validate email format using regex
    if not re.match(email_regex, email):
        return jsonify({'error': 'Invalid email format'}), 400

    # Insert into database
    new_subscriber = Subscriber(name=name, email=email)
    try:
        db.session.add(new_subscriber)
        db.session.commit()
        return jsonify({'message': 'Subscribed successfully!'}), 201
    except IntegrityError:
        db.session.rollback()  # Roll back the session in case of dupe error
        return jsonify({'error': 'Email already exists'}), 409
    except Exception as e:
        db.session.rollback()  # Roll back the session in case of generic error
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
