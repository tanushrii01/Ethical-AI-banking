"""
init_db.py — Run this ONCE on Render (via Shell) after first deploy to create tables.

Usage:
    python init_db.py

On Render Shell:
    python init_db.py
"""
from app import app
from models import db

with app.app_context():
    db.create_all()
    print("[OK] All database tables created successfully.")
    print(f"[OK] Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
