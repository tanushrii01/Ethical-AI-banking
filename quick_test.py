import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Starting test...")
try:
    from app import app
    from models import db, User
    print("Imports successful!")
    
    with app.app_context():
        print("\nChecking database...")
        users = User.query.all()
        print(f"Found {len(users)} users")
        
        admin = User.query.filter_by(email='admin@trustbank.com').first()
        if admin:
            print(f"\nAdmin user exists: {admin.email}")
            if admin.check_password('admin123'):
                print("Password 'admin123' works!")
            else:
                print("Password 'admin123' does NOT work!")
        else:
            print("\nAdmin user NOT found - creating it...")
            admin = User(name='Admin User', email='admin@trustbank.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created!")
        
        print("\nAll users:")
        for u in User.query.all():
            print(f"  - {u.email}")
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

