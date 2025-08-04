#!/usr/bin/env python3
"""
Flask Application Runner for VeriSure Blockchain Certification
This script runs the Flask version of the application alongside the existing Streamlit app.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("✓ Flask dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing Flask dependency: {e}")
        print("Please install Flask dependencies:")
        print("pip install -r requirements_flask.txt")
        return False

def check_blockchain_connection():
    """Check if blockchain connection is available"""
    try:
        from connection import w3
        if w3.is_connected():
            print("✓ Blockchain connection established")
            return True
        else:
            print("⚠ Blockchain not connected - make sure Ganache is running")
            return False
    except Exception as e:
        print(f"⚠ Blockchain connection error: {e}")
        return False

def main():
    """Main function to run the Flask application"""
    print("=" * 50)
    print("VeriSure Flask Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check blockchain connection
    check_blockchain_connection()
    
    # Change to application directory
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    print("\nStarting Flask application...")
    print("Flask app will be available at: http://localhost:5000")
    print("Streamlit app can still be run separately at: http://localhost:8501")
    print("\nPress Ctrl+C to stop the Flask application")
    print("-" * 50)
    
    try:
        # Import and run the Flask app
        from flask_app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nFlask application stopped by user")
    except Exception as e:
        print(f"Error running Flask application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 