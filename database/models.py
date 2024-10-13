from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import ValidationConfig

db = SQLAlchemy()

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(ValidationConfig.MAX_NAME_LEN), nullable=False)
    email = db.Column(db.String(ValidationConfig.MAX_EMAIL_LEN), nullable=False, unique=True)
    subscribed_date = db.Column(db.DateTime, default=datetime.utcnow)  # Subscribed date field

    def __repr__(self):
        return f'<Subscriber {self.name}>'