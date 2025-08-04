from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_cors import CORS
import json
from pathlib import Path
from web3 import Web3
import base64
from PIL import Image
import io
import os
import hashlib
import requests
from dotenv import load_dotenv

# Import your existing utilities and database functions
from connection import w3, contract, contract_abi
from utils.cert_utils import generate_certificate, extract_certificate
from db.firebase_app import login, register

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
CORS(app)

load_dotenv()

# Environment variables
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_API_SECRET = os.getenv("PINATA_API_SECRET")
INSTITUTE_EMAIL = os.getenv("institute_email")
INSTITUTE_PASSWORD = os.getenv("institute_password")

def upload_to_pinata(file_path, api_key, api_secret):
    """Upload file to Pinata IPFS - same as your Streamlit code"""
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}
        response = requests.post(pinata_api_url, headers=headers, files=files)
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None

def display_pdf_html(file_path):
    """Convert PDF to HTML display - equivalent to your displayPDF function"""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

def view_certificate_flask(certificate_id):
    """View certificate from blockchain - equivalent to your view_certificate function"""
    try:
        result = contract.functions.getCertificate(certificate_id).call()
        # Check if the certificate exists: UID and IPFS hash should not be empty or default
        if not result or not result[0] or not result[4] or result[4] in ('', '0', '0x0', None):
            raise Exception("Certificate not found on blockchain.")
        ipfs_hash = result[4]
        pinata_gateway_base_url = 'https://gateway.pinata.cloud/ipfs'
        content_url = f"{pinata_gateway_base_url}/{ipfs_hash}"
        response = requests.get(content_url)
        temp_file = "temp.pdf"
        with open(temp_file, 'wb') as pdf_file:
            pdf_file.write(response.content)
        pdf_html = display_pdf_html(temp_file)
        os.remove(temp_file)
        return pdf_html
    except Exception as e:
        raise  # Let the outer try/except in the API handle the error

# Route for the main page
@app.route('/')
def main_page():
    """Main page route - now uses template"""
    return render_template('index.html')

# Route to serve the main logo
@app.route('/logo')
def serve_logo():
    """Serve the main logo"""
    logo_path = os.path.join(app.root_path, 'assets', 'company_logo.jpg')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = f.read()
        return logo_data, 200, {'Content-Type': 'image/jpeg'}
    else:
        return "Logo not found", 404

# Route to serve the institute logo
@app.route('/institute-logo')
def serve_institute_logo():
    """Serve the institute logo"""
    logo_path = os.path.join(app.root_path, 'assets', 'institute_logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = f.read()
        return logo_data, 200, {'Content-Type': 'image/png'}
    else:
        return "Logo not found", 404

# Route to serve the verifier logo
@app.route('/verifier-logo')
def serve_verifier_logo():
    """Serve the verifier logo"""
    logo_path = os.path.join(app.root_path, 'assets', 'Myverifiers.gif')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = f.read()
        return logo_data, 200, {'Content-Type': 'image/gif'}
    else:
        return "Logo not found", 404

# API endpoint to set user role
@app.route('/api/set-role', methods=['POST'])
def set_role():
    """Set user role in session"""
    data = request.get_json()
    role = data.get('role')
    if role in ['institute', 'verifier']:
        session['profile'] = role.capitalize()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid role'})

# Register page route
@app.route('/register')
def register_page():
    """Register page route - now uses template"""
    return render_template('register.html')

# API endpoint for registration
@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for user registration"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        result = register(email, password)
        if result:
            return jsonify({
                'success': True,
                'message': 'Registration successful!',
                'redirect': '/login'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Registration failed'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Login page route
@app.route('/login')
def login_page():
    """Login page route - now uses template"""
    user_profile = session.get('profile', 'Institute')
    return render_template('login.html', user_profile=user_profile)

# API endpoint for login
@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for user login"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        result = login(email, password)
        if result:
            session['user_email'] = email
            user_profile = session.get('profile', 'Institute')
            
            if user_profile == 'Institute':
                return jsonify({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect': '/institute-dashboard'
                })
            else:
                return jsonify({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect': '/verifier-dashboard'
                })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Institute dashboard route
@app.route('/institute-dashboard')
def institute_dashboard():
    """Institute dashboard page - now uses template"""
    return render_template('institute_dashboard.html')

# Verifier dashboard route
@app.route('/verifier-dashboard')
def verifier_dashboard():
    """Verifier dashboard page - now uses template"""
    return render_template('verifier_dashboard.html')

# API endpoint for generating certificates
@app.route('/api/generate-certificate', methods=['POST'])
def generate_certificate_api():
    """API endpoint for generating certificates"""
    data = request.get_json()
    uid = data.get('uid')
    candidate_name = data.get('candidateName')
    course_name = data.get('courseName')
    org_name = data.get('orgName')
    
    try:
        # Generate certificate using your existing utility
        certificate_path = generate_certificate(uid, candidate_name, course_name, org_name)
        
        # Upload to IPFS
        ipfs_hash = upload_to_pinata(certificate_path, PINATA_API_KEY, PINATA_API_SECRET)
        
        if ipfs_hash:
            # Issue certificate on blockchain
            certificate_id = issue_certificate_on_blockchain(uid, candidate_name, course_name, org_name, ipfs_hash)
            
            return jsonify({
                'success': True,
                'message': 'Certificate generated successfully!',
                'certificateId': certificate_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to upload certificate to IPFS'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# API endpoint for viewing certificates
@app.route('/api/view-certificate', methods=['POST'])
def view_certificate_api():
    """API endpoint for viewing certificates"""
    data = request.get_json()
    certificate_id = data.get('certificateId')
    
    try:
        pdf_html = view_certificate_flask(certificate_id)
        return jsonify({
            'success': True,
            'pdfHtml': pdf_html
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Function to issue certificate on blockchain
def issue_certificate_on_blockchain(uid, candidate_name, course_name, org_name, ipfs_hash):
    """Issue certificate on blockchain"""
    try:
        # This would be your blockchain interaction code
        # For now, we'll generate a simple hash as certificate ID
        certificate_data = f"{uid}{candidate_name}{course_name}{org_name}{ipfs_hash}"
        certificate_id = hashlib.sha256(certificate_data.encode()).hexdigest()[:16]
        return certificate_id
    except Exception as e:
        raise Exception(f"Failed to issue certificate on blockchain: {str(e)}")

# API endpoint for issuing certificates
@app.route('/api/issue-certificate', methods=['POST'])
def issue_certificate():
    """API endpoint for issuing certificates on blockchain"""
    data = request.get_json()
    uid = data.get('uid')
    candidate_name = data.get('candidateName')
    course_name = data.get('courseName')
    org_name = data.get('orgName')
    ipfs_hash = data.get('ipfsHash')
    
    try:
        certificate_id = issue_certificate_on_blockchain(uid, candidate_name, course_name, org_name, ipfs_hash)
        return jsonify({
            'success': True,
            'certificateId': certificate_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# API endpoint to get all certificates
@app.route('/api/certificates')
def get_certificates():
    """API endpoint to get all certificates from the blockchain"""
    try:
        # Assuming the contract has a function to get all certificate IDs
        cert_ids = contract.functions.getAllCertificateIds().call()
        certificates = []
        for cert_id in cert_ids:
            result = contract.functions.getCertificate(cert_id).call()
            # Only include if valid (not empty)
            if result and result[0] and result[4] and result[4] not in ('', '0', '0x0', None):
                certificates.append({
                    'certificate_id': cert_id,
                    'uid': result[0],
                    'candidate_name': result[1],
                    'course_name': result[2],
                    'org_name': result[3],
                    'ipfs_hash': result[4]
                })
        return jsonify({'success': True, 'certificates': certificates})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API endpoint for verifying PDF certificates
@app.route('/api/verify-pdf', methods=['POST'])
def verify_pdf():
    """API endpoint for verifying PDF certificates"""
    if 'pdf_file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file uploaded'
        })
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        })
    
    try:
        # Save uploaded file temporarily
        temp_path = "temp_upload.pdf"
        file.save(temp_path)
        
        # Extract certificate data
        extracted_data = extract_certificate(temp_path)
        
        # Verify against blockchain (simplified for now)
        verified = True  # This would be your verification logic
        
        # Generate PDF HTML for display
        pdf_html = display_pdf_html(temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'verified': verified,
            'extractedData': extracted_data,
            'pdfHtml': pdf_html,
            'mismatchedFields': []  # This would contain any mismatched fields
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# API endpoint for verifying certificate by ID
@app.route('/api/verify-certificate-id', methods=['POST'])
def verify_certificate_id():
    """API endpoint for verifying certificate by ID"""
    data = request.get_json()
    certificate_id = data.get('certificateId')
    try:
        pdf_html = view_certificate_flask(certificate_id)
        return jsonify({
            'success': True,
            'pdfHtml': pdf_html
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# API endpoint for verifying certificates
@app.route('/api/verify-certificate', methods=['POST'])
def verify_certificate():
    """API endpoint for verifying certificates"""
    data = request.get_json()
    certificate_id = data.get('certificateId')
    
    try:
        # This would be your certificate verification logic
        verified = True  # Simplified for now
        return jsonify({
            'success': True,
            'verified': verified
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# API endpoint for blockchain status
@app.route('/api/blockchain-status')
def blockchain_status():
    """API endpoint for blockchain status"""
    try:
        # Check blockchain connection
        latest_block = w3.eth.block_number
        return jsonify({
            'success': True,
            'connected': True,
            'latestBlock': latest_block
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'connected': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 