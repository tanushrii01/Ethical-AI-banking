#!/usr/bin/env python
"""Quick check to verify the Flask app is set up correctly"""
import sys
import os

print("=" * 60)
print("TrustBank AI - Application Check")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version.split()[0]}")

# Check if we're in the right directory
if not os.path.exists('app.py'):
    print("\n✗ ERROR: app.py not found!")
    print("   Make sure you're in the Ethical-AI-banking directory")
    sys.exit(1)
print("\n✓ Found app.py")

# Try importing
try:
    from app import app
    print("✓ App imported successfully")
except Exception as e:
    print(f"\n✗ ERROR importing app: {e}")
    sys.exit(1)

# Check routes
print("\n✓ Available routes:")
routes = []
for rule in sorted(app.url_map.iter_rules(), key=lambda x: x.rule):
    if rule.rule != '/static/<path:filename>':
        routes.append(rule.rule)
        print(f"   {rule.rule}")

if len(routes) < 5:
    print("\n⚠ WARNING: Not enough routes found!")
else:
    print(f"\n✓ Found {len(routes)} routes")

# Check database
try:
    from models import db, User
    with app.app_context():
        users = User.query.all()
        print(f"\n✓ Database connected - {len(users)} users found")
        if len(users) == 0:
            print("   (No users yet - this is normal for first run)")
except Exception as e:
    print(f"\n⚠ Database warning: {e}")

# Check templates
templates_dir = 'templates'
if os.path.exists(templates_dir):
    templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
    print(f"\n✓ Found {len(templates)} HTML templates")
    if 'login.html' not in templates:
        print("   ⚠ WARNING: login.html not found!")
else:
    print("\n✗ ERROR: templates directory not found!")

# Check static files
static_dir = 'static'
if os.path.exists(static_dir):
    static_files = os.listdir(static_dir)
    print(f"\n✓ Found {len(static_files)} static files")
else:
    print("\n⚠ WARNING: static directory not found!")

print("\n" + "=" * 60)
print("CHECK COMPLETE")
print("=" * 60)
print("\nTo start the server, run:")
print("  python app.py")
print("\nThen open: http://127.0.0.1:5000")

