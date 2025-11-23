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
                    print("Column 'explanation' already exists.")
                else:
                    print("Adding 'explanation' column...")
                    conn.execute(text("ALTER TABLE loan_application ADD COLUMN explanation TEXT"))
                    conn.commit()
                    print("Successfully added 'explanation' column.")
                    
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
