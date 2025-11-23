#!/usr/bin/env python
"""Run script for the Flask application"""
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("TrustBank AI - Starting Flask Application")
    print("=" * 50)
    print("\nServer will be available at:")
    print("  http://127.0.0.1:5000")
    print("  http://localhost:5000")
    print("\nAvailable routes:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda x: x.rule):
        if rule.rule != '/static/<path:filename>':
            print(f"  {rule.rule}")
    print("\n" + "=" * 50)
    print("Starting server...\n")
    app.run(debug=True, host='127.0.0.1', port=5000)

