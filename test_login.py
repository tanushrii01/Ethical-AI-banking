#!/usr/bin/env python
"""Test script to verify login functionality"""
from app import app
from models import db, User

with app.app_context():
    print("=" * 60)
    print("LOGIN TEST")
    print("=" * 60)
    
    # Check for admin user
    admin = User.query.filter_by(email='admin@trustbank.com').first()
    if admin:
        print(f"\n✓ Admin user found: {admin.email}")
        print(f"  Name: {admin.name}")
        print(f"  Is Admin: {admin.is_admin}")
        
        # Test password
        if admin.check_password('admin123'):
            print("  ✓ Password 'admin123' is correct")
        else:
            print("  ✗ Password 'admin123' is INCORRECT")
    else:
        print("\n✗ Admin user NOT found!")
        print("  Creating admin user...")
        admin = User(name='Admin User', email='admin@trustbank.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("  ✓ Admin user created: admin@trustbank.com / admin123")
    
    # List all users
    print("\nAll users in database:")
    users = User.query.all()
    for u in users:
        print(f"  - {u.email} ({u.name}) - Admin: {u.is_admin}")
    
    print("\n" + "=" * 60)
    print("To test login:")
    print("1. Go to http://127.0.0.1:5000/login")
    print("2. Use: admin@trustbank.com / admin123")
    print("=" * 60)

