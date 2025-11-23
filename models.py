from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    loans = db.relationship('LoanApplication', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    income = db.Column(db.Float, nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    employment_years = db.Column(db.Float, nullable=False)
    debt_to_income = db.Column(db.Float, nullable=False)
    model_decision = db.Column(db.String(50))
    model_confidence = db.Column(db.Float)
    human_override = db.Column(db.String(50))
    explanation = db.Column(db.Text, nullable=True)  # Store rejection reasons or approval notes
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_db(app):
    with app.app_context():
        db.create_all()
        # Create default admin user if it doesn't exist
        if not User.query.filter_by(email='admin@trustbank.com').first():
            admin = User(
                name='Admin User',
                email='admin@trustbank.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Created default admin: admin@trustbank.com / admin123")
