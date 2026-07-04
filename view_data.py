"""
view_data.py  — Quick read-only peek at the local SQLite database.
Run with:  python view_data.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "instance", "app.sqlite")

if not os.path.exists(DB_PATH):
    print(f"[ERROR] Database not found at: {DB_PATH}")
    exit(1)

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# ── Tables ────────────────────────────────────────────────────────────────────
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("=" * 60)
print("TABLES:", tables)

# ── Users ─────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("USERS")
print("=" * 60)
cur.execute("SELECT id, name, email, is_admin FROM user")
rows = cur.fetchall()
if rows:
    print(f"  {'ID':<5} {'Name':<20} {'Email':<30} {'Admin'}")
    print("  " + "-" * 58)
    for r in rows:
        print(f"  {r[0]:<5} {r[1]:<20} {r[2]:<30} {bool(r[3])}")
else:
    print("  (no users)")

# ── Loan Applications ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("LOAN APPLICATIONS")
print("=" * 60)
cur.execute("""
    SELECT id, user_id, amount, income, credit_score,
           debt_to_income, employment_years,
           model_decision, model_confidence, submitted_at
    FROM loan_application
    ORDER BY submitted_at DESC
""")
loans = cur.fetchall()
if loans:
    for r in loans:
        print(f"\n  Loan #{r[0]}")
        print(f"    User ID       : {r[1]}")
        print(f"    Amount        : Rs.{r[2]:,.0f}")
        print(f"    Income        : Rs.{r[3]:,.0f}")
        print(f"    Credit Score  : {r[4]}")
        print(f"    Debt/Income   : {r[5]*100:.1f}%")
        print(f"    Emp. Years    : {r[6]}")
        print(f"    Decision      : {r[7]}  (confidence {r[8]*100:.0f}%)" if r[8] else f"    Decision      : {r[7]}")
        print(f"    Submitted     : {r[9]}")
else:
    print("  (no loan applications yet)")

con.close()
print("\n" + "=" * 60)
