import re
from flask import Blueprint, request, jsonify
from database.models import db, Subscriber
from config import ValidationConfig
from sqlalchemy.exc import IntegrityError

subscribe_bp = Blueprint('subscribe', __name__)

api_cors_config = {
  "origins": "*",
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Authorization", "Content-Type"]
}

# Regex pattern for email validation
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@subscribe_bp.route('/subscribe', methods=['POST'])
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
    
@subscribe_bp.route('/subscribe', methods=['OPTIONS'])
def preflight():
    response = jsonify()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response, 200