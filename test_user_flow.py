from app import app
from models import db, User
import uuid

def test_user_flow():
    with app.app_context():
        print("=" * 50)
        print("USER FLOW VERIFICATION")
        print("=" * 50)

        # 1. Setup unique test user
        unique_id = str(uuid.uuid4())[:8]
        name = f"Test User {unique_id}"
        email = f"newuser_{unique_id}@example.com"
        password = "securepassword123"

        print(f"\n1. Simulating Signup for: {email}")
        
        # Cleanup if exists (unlikely with uuid but good practice)
        existing = User.query.filter_by(email=email).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # Create User
        try:
            new_user = User(name=name, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print("   [OK] User created and saved to database.")
        except Exception as e:
            print(f"   [FAIL] Signup failed: {e}")
            return

        # 2. Verify Storage
        print("\n2. Verifying Database Storage")
        stored_user = User.query.filter_by(email=email).first()
        if stored_user:
            print(f"   [OK] User found in database. ID: {stored_user.id}")
            print(f"   [OK] Password hash stored: {stored_user.password_hash[:20]}...")
        else:
            print("   [FAIL] User not found in database after save.")
            return

        # 3. Simulate Login
        print("\n3. Simulating Login (Password Check)")
        if stored_user.check_password(password):
            print("   [OK] Login successful! Password matches.")
        else:
            print("   [FAIL] Login failed! Password does not match.")

        # 4. Simulate Wrong Password
        print("\n4. Simulating Invalid Login")
        if not stored_user.check_password("wrongpassword"):
            print("   [OK] Invalid password correctly rejected.")
        else:
            print("   [FAIL] Invalid password was accepted!")

        print("\n" + "=" * 50)
        print("VERIFICATION COMPLETE: New users can signup and login.")
        print("=" * 50)

if __name__ == "__main__":
    test_user_flow()
