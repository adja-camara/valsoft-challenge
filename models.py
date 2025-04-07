from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sessions = db.relationship('CustomerSession', backref='customer', lazy=True)

class CustomerSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    happiness_score = db.Column(db.Float, nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    service_time = db.Column(db.Float)  # in seconds
    server_name = db.Column(db.String(100))
    order_details = db.Column(db.String(500))
    exit_time = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer.name,
            'happiness_score': self.happiness_score,
            'entry_time': self.entry_time.isoformat(),
            'service_time': self.service_time,
            'server_name': self.server_name,
            'order_details': self.order_details,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None
        } 