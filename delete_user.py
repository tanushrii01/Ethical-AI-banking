from app import app, db
from models import User, LoanApplication

def delete_specific_user():
    target_email = "yukthir739@gmail.gcom"
    
    with app.app_context():
        print("=" * 50)
        print(f"DELETING USER: {target_email}")
        print("=" * 50)
        
        user = User.query.filter_by(email=target_email).first()
        
        if user:
            print(f"   [FOUND] User found with ID: {user.id}, Name: {user.name}")
            
            # Delete associated loans first (if cascade isn't set up perfectly)
            loans = LoanApplication.query.filter_by(user_id=user.id).all()
            if loans:
                print(f"   [INFO] Deleting {len(loans)} associated loan applications...")
                for loan in loans:
                    db.session.delete(loan)
            
            # Delete the user
            db.session.delete(user)
            try:
                db.session.commit()
                print(f"   [SUCCESS] User {target_email} and their data have been deleted.")
            except Exception as e:
                db.session.rollback()
                print(f"   [ERROR] Failed to delete user: {e}")
        else:
            print(f"   [INFO] User {target_email} not found in the database. Nothing to delete.")

if __name__ == "__main__":
    delete_specific_user()
