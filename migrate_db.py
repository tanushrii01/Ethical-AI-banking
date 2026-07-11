from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        print("Checking database schema...")
        try:
            # Check if column exists
            with db.engine.connect() as conn:
                result = conn.execute(text("PRAGMA table_info(loan_application)"))
                columns = [row.name for row in result]
                
                if 'explanation' in columns:
                    print("Column 'explanation' already exists in loan_application.")
                else:
                    print("Adding 'explanation' column to loan_application...")
                    conn.execute(text("ALTER TABLE loan_application ADD COLUMN explanation TEXT"))
                    conn.commit()
                    print("Successfully added 'explanation' column to loan_application.")
                
                # Check user table for spending column
                result_user = conn.execute(text("PRAGMA table_info(user)"))
                user_columns = [row.name for row in result_user]
                
                if 'spending' in user_columns:
                    print("Column 'spending' already exists in user.")
                else:
                    print("Adding 'spending' column to user...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN spending FLOAT DEFAULT 0.0"))
                    conn.commit()
                    print("Successfully added 'spending' column to user.")
                    
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
