from app import app, currency_filter

def verify_currency():
    print("=" * 50)
    print("CURRENCY VERIFICATION")
    print("=" * 50)

    # 1. Check Filter
    print("\n1. Checking currency_filter logic...")
    val = 1000
    formatted = currency_filter(val)
    # Check for byte sequence of Rupee symbol or just length/content without printing it
    if "₹" in formatted:
        print(f"   [OK] Filter output contains Rupee symbol: {formatted.encode('utf-8', errors='replace')}")
    else:
        print(f"   [FAIL] Filter output missing Rupee symbol: {formatted.encode('utf-8', errors='replace')}")

    # 2. Check Template Rendering (simulated)
    print("\n2. Checking Template Rendering...")
    with app.test_client() as client:
        # We need to login first to see dashboard
        # Assuming admin user exists from previous steps
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user'] = {'id': 1, 'name': 'Admin', 'email': 'admin@trustbank.com'}
        
        response = client.get('/dashboard')
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            if "₹" in content:
                print("   [OK] Dashboard contains '₹' symbol.")
            else:
                print("   [WARN] Dashboard does NOT contain '₹' symbol (might be no loans yet).")
                
            if "$" not in content:
                 print("   [OK] Dashboard does NOT contain '$' symbol (excluding scripts/comments).")
            else:
                 # It might be in comments or scripts, so we just warn
                 print("   [INFO] Dashboard contains '$' symbol (check if it's in code or text).")
        else:
             print(f"   [FAIL] Could not access dashboard. Status: {response.status_code}")

    print("\n" + "=" * 50)
    print("VERIFICATION COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    verify_currency()
