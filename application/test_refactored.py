#!/usr/bin/env python3
"""
Test script for the refactored Flask application
"""

import requests
import json
import time

def test_flask_app():
    """Test the refactored Flask application"""
    base_url = "http://localhost:5000"
    
    print("Testing Refactored Flask Application")
    print("=" * 50)
    
    # Test 1: Main page
    print("\n1. Testing main page...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✓ Main page loads successfully")
        else:
            print(f"✗ Main page failed with status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to Flask app. Make sure it's running on port 5000")
        return False
    
    # Test 2: Register page
    print("\n2. Testing register page...")
    try:
        response = requests.get(f"{base_url}/register")
        if response.status_code == 200:
            print("✓ Register page loads successfully")
        else:
            print(f"✗ Register page failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Register page test failed: {e}")
    
    # Test 3: Login page
    print("\n3. Testing login page...")
    try:
        response = requests.get(f"{base_url}/login")
        if response.status_code == 200:
            print("✓ Login page loads successfully")
        else:
            print(f"✗ Login page failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Login page test failed: {e}")
    
    # Test 4: Institute dashboard
    print("\n4. Testing institute dashboard...")
    try:
        response = requests.get(f"{base_url}/institute-dashboard")
        if response.status_code == 200:
            print("✓ Institute dashboard loads successfully")
        else:
            print(f"✗ Institute dashboard failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Institute dashboard test failed: {e}")
    
    # Test 5: Verifier dashboard
    print("\n5. Testing verifier dashboard...")
    try:
        response = requests.get(f"{base_url}/verifier-dashboard")
        if response.status_code == 200:
            print("✓ Verifier dashboard loads successfully")
        else:
            print(f"✗ Verifier dashboard failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Verifier dashboard test failed: {e}")
    
    # Test 6: Static files
    print("\n6. Testing static files...")
    try:
        response = requests.get(f"{base_url}/static/css/main.css")
        if response.status_code == 200:
            print("✓ CSS file loads successfully")
        else:
            print(f"✗ CSS file failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ CSS file test failed: {e}")
    
    try:
        response = requests.get(f"{base_url}/static/js/main.js")
        if response.status_code == 200:
            print("✓ JavaScript file loads successfully")
        else:
            print(f"✗ JavaScript file failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ JavaScript file test failed: {e}")
    
    # Test 7: Logo files
    print("\n7. Testing logo files...")
    try:
        response = requests.get(f"{base_url}/logo")
        if response.status_code == 200:
            print("✓ Main logo loads successfully")
        else:
            print(f"✗ Main logo failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Main logo test failed: {e}")
    
    try:
        response = requests.get(f"{base_url}/institute-logo")
        if response.status_code == 200:
            print("✓ Institute logo loads successfully")
        else:
            print(f"✗ Institute logo failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Institute logo test failed: {e}")
    
    try:
        response = requests.get(f"{base_url}/verifier-logo")
        if response.status_code == 200:
            print("✓ Verifier logo loads successfully")
        else:
            print(f"✗ Verifier logo failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Verifier logo test failed: {e}")
    
    # Test 8: API endpoints
    print("\n8. Testing API endpoints...")
    
    # Test set-role API
    try:
        response = requests.post(f"{base_url}/api/set-role", 
                               json={"role": "institute"},
                               headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✓ Set role API works successfully")
            else:
                print(f"✗ Set role API failed: {data.get('error')}")
        else:
            print(f"✗ Set role API failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Set role API test failed: {e}")
    
    # Test blockchain status API
    try:
        response = requests.get(f"{base_url}/api/blockchain-status")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✓ Blockchain status API works successfully")
            else:
                print(f"✗ Blockchain status API failed: {data.get('error')}")
        else:
            print(f"✗ Blockchain status API failed with status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Blockchain status API test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Testing completed!")
    print("\nTo run the application:")
    print("1. Make sure you have all dependencies installed")
    print("2. Run: python flask_app_refactored.py")
    print("3. Open your browser to: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    test_flask_app() 