#!/usr/bin/env python
"""Quick test script to verify database and login functionality"""
from app import app
from models import db, User, LoanApplication
from werkzeug.security import check_password_hash

with app.app_context():
    print("=" * 50)
    print("DATABASE TEST")
    print("=" * 50)
    
    # Check if database exists
    print("\n1. Checking database connection...")
    try:
        users = User.query.all()
        print(f"   [OK] Database connected. Found {len(users)} users")
    except Exception as e:
        print(f"   [ERROR] Database error: {e}")
        exit(1)
    
    # List all users
    print("\n2. Users in database:")
    if users:
        for user in users:
            print(f"   - {user.name} ({user.email}) - Admin: {user.is_admin}")
    else:
        print("   No users found. Creating test user...")
        test_user = User(name="Test User", email="test@example.com", is_admin=False)
        test_user.set_password("test123")
        db.session.add(test_user)
        db.session.commit()
        print("   [OK] Test user created: test@example.com / test123")
    
    # Test password checking
    print("\n3. Testing password verification...")
    admin = User.query.filter_by(email='admin@trustbank.com').first()
    if admin:
        if admin.check_password('admin123'):
            print("   [OK] Admin password works correctly")
        else:
            print("   [FAIL] Admin password check failed")
    else:
        print("   [WARN] Admin user not found")
    
    # Check loans
    print("\n4. Loan applications:")
    loans = LoanApplication.query.all()
    print(f"   Found {len(loans)} loan applications")
    for loan in loans[:5]:  # Show first 5
        user = User.query.get(loan.user_id)
        print(f"   - Loan #{loan.id}: ${loan.amount:,.0f} by {user.name if user else 'Unknown'} - Status: {loan.model_decision or 'PENDING'}")
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)
    print("\nTo test login:")
    print("1. Go to http://127.0.0.1:5000/login")
    print("2. Use admin@trustbank.com / admin123")
    print("3. Or create a new account via signup")

