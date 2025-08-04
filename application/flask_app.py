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
        return f"Error viewing certificate: {str(e)}"

# HTML template for the main page
MAIN_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>VeriSure - Blockchain Certification</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }
        .logo {
            width: 600px;
            margin: 20px auto;
        }
        .role-selection {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 40px;
        }
        .role-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.2s;
        }
        .role-card:hover {
            transform: translateY(-5px);
        }
        .role-card img {
            width: 270px;
            height: auto;
            margin-bottom: 15px;
        }
        .role-card h3 {
            margin: 0;
            color: #333;
        }
        .wallet-info {
            margin-top: 20px;
            padding: 10px;
            background: #e8f5e8;
            border-radius: 5px;
        }
        .button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        .button:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="/logo" alt="VeriSure Logo" style="width: 100%;">
        </div>
        
        <h2>Select Your Role</h2>
        
        <div class="role-selection">
            <div class="role-card" onclick="selectRole('institute')">
                <img src="/institute-logo" alt="Institute">
                <h3>Institute</h3>
            </div>
            <div class="role-card" onclick="selectRole('verifier')">
                <img src="/verifier-logo" alt="Verifier">
                <h3>Verifier</h3>
            </div>
        </div>
        
        <div class="wallet-info">
            <p id="wallet">Not connected</p>
            <button class="button" onclick="connectMetaMask()">Connect MetaMask</button>
        </div>
    </div>

    <script>
        async function connectMetaMask() {
            if (typeof window.ethereum !== 'undefined') {
                console.log('MetaMask is installed!');
                try {
                    await window.ethereum.request({ method: 'eth_requestAccounts' });
                    const account = window.ethereum.selectedAddress;
                    document.getElementById('wallet').textContent = "Connected: " + account;
                } catch (error) {
                    console.error("Error connecting to MetaMask:", error);
                    alert('Connection failed.');
                }
            } else {
                alert('MetaMask not installed!');
                document.getElementById('wallet').textContent = "MetaMask not installed";
            }
        }

        function selectRole(role) {
            // Store role in session and redirect to appropriate page
            fetch('/api/set-role', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({role: role})
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/login';
                }
            });
        }
    </script>
</body>
</html>
"""

# Session management is handled by Flask session

@app.route('/')
def main_page():
    """Main page route - serves the role selection page"""
    return render_template('index.html')

@app.route('/logo')
def serve_logo():
    """Serve the main logo GIF"""
    try:
        gif_path = "assets/VerifyLabPro.gif"
        if os.path.exists(gif_path):
            with open(gif_path, 'rb') as f:
                gif_data = f.read()
            return gif_data, 200, {'Content-Type': 'image/gif'}
        else:
            return "Logo not found", 404
    except Exception as e:
        return str(e), 500

@app.route('/institute-logo')
def serve_institute_logo():
    """Serve the institute logo"""
    try:
        logo_path = "../assets/MyIns.png"
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            return logo_data, 200, {'Content-Type': 'image/png'}
        else:
            return "Logo not found", 404
    except Exception as e:
        return str(e), 500

@app.route('/verifier-logo')
def serve_verifier_logo():
    """Serve the verifier logo"""
    try:
        logo_path = "../assets/VerifiersLog.jpg"
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            return logo_data, 200, {'Content-Type': 'image/jpeg'}
        else:
            return "Logo not found", 404
    except Exception as e:
        return str(e), 500

@app.route('/api/set-role', methods=['POST'])
def set_role():
    """API endpoint to set user role"""
    try:
        data = request.get_json()
        role = data.get('role')
        if role in ['institute', 'verifier']:
            session['profile'] = 'Institute' if role == 'institute' else 'Verifier'
            return jsonify({'success': True, 'role': role})
        else:
            return jsonify({'success': False, 'error': 'Invalid role'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/register')
def register_page():
    """Register page route"""
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for registration - exact same logic as your Streamlit register"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_profile = session.get('profile', 'Institute')
        
        # Use your existing Firebase register function
        result = register(email, password)
        if result == "success":
            session['logged_in'] = True
            session['user_type'] = 'verifier'
            
            # Same redirect logic as your Streamlit code
            if user_profile == "Institute":
                return jsonify({
                    'success': True, 
                    'redirect': '/institute-dashboard'
                })
            else:
                return jsonify({
                    'success': True, 
                    'redirect': '/verifier-dashboard'
                })
        else:
            return jsonify({'success': False, 'error': 'Registration unsuccessful!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/login')
def login_page():
    """Login page route"""
    user_profile = session.get('profile', 'Institute')
    return render_template('login.html', user_profile=user_profile)

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for login - exact same logic as your Streamlit login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_profile = session.get('profile', 'Institute')
        
        # Exact same logic as your Streamlit login
        if user_profile == "Institute":
            valid_email = INSTITUTE_EMAIL
            valid_pass = INSTITUTE_PASSWORD
            if email == valid_email and password == valid_pass:
                session['logged_in'] = True
                session['user_type'] = 'institute'
                return jsonify({
                    'success': True, 
                    'redirect': '/institute-dashboard'
                })
            else:
                return jsonify({'success': False, 'error': 'Invalid credentials!'}), 401
        else:
            # Use your existing Firebase login function
            result = login(email, password)
            if result == "success":
                session['logged_in'] = True
                session['user_type'] = 'verifier'
                return jsonify({
                    'success': True, 
                    'redirect': '/verifier-dashboard'
                })
            else:
                return jsonify({'success': False, 'error': 'Invalid credentials!'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/institute-dashboard')
def institute_dashboard():
    """Institute dashboard page"""
    return render_template('institute_dashboard.html')

@app.route('/verifier-dashboard')
def verifier_dashboard():
    """Verifier dashboard page"""
    return render_template('verifier_dashboard.html')

# API endpoints for blockchain interactions - exact same functionality as your Streamlit code
@app.route('/api/generate-certificate', methods=['POST'])
def generate_certificate_api():
    """API endpoint to generate certificate - exact same logic as your Streamlit institute"""
    try:
        data = request.get_json()
        uid = data.get('uid')
        candidate_name = data.get('candidateName')
        course_name = data.get('courseName')
        org_name = data.get('orgName')
        
        # Exact same logic as your Streamlit code
        pdf_file_path = "certificate.pdf"
        logo_path = r"D:\gnane\Downloads\nonservicable.jpeg"
        
        # Generate certificate using your existing function
        generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, logo_path)

        # Upload the PDF to Pinata using your existing function
        ipfs_hash = upload_to_pinata(pdf_file_path, PINATA_API_KEY, PINATA_API_SECRET)
        os.remove(pdf_file_path)
        
        # Generate certificate ID using your exact same logic
        data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest() 

        # Smart Contract Call - exact same as your Streamlit code
        contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash).transact({'from': w3.eth.accounts[0]})
        
        print(f"[DEBUG] Certificate ID generated: {certificate_id}")
        
        return jsonify({
            'success': True, 
            'certificateId': certificate_id,
            'message': f"Certificate successfully generated with Certificate ID: {certificate_id}"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/view-certificate', methods=['POST'])
def view_certificate_api():
    """API endpoint to view certificate - exact same logic as your Streamlit institute"""
    try:
        data = request.get_json()
        certificate_id = data.get('certificateId')
        
        print(f"[DEBUG] Certificate ID entered for verification: {certificate_id}")
        
        # Exact same logic as your Streamlit code
        is_verified = contract.functions.isVerified(certificate_id).call()
        if not is_verified:
            return jsonify({'success': False, 'error': 'Certificate ID not found on blockchain.'}), 404
        else:
            try:
                pdf_html = view_certificate_flask(certificate_id)
                return jsonify({
                    'success': True, 
                    'pdfHtml': pdf_html
                })
            except Exception as e:
                return jsonify({'success': False, 'error': 'Invalid Certificate ID!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/issue-certificate', methods=['POST'])
def issue_certificate():
    """API endpoint to issue a new certificate on blockchain"""
    try:
        data = request.get_json()
        student_name = data.get('studentName')
        course_name = data.get('courseName')
        grade = data.get('grade')
        date = data.get('date')
        
        # Here you would interact with your smart contract
        # For now, we'll simulate the blockchain interaction
        certificate_data = {
            'studentName': student_name,
            'courseName': course_name,
            'grade': grade,
            'date': date,
            'id': f"cert_{len(get_certificates()) + 1}"
        }
        
        # In a real implementation, you would:
        # 1. Call the smart contract function
        # 2. Wait for transaction confirmation
        # 3. Store the certificate data
        
        return jsonify({'success': True, 'certificate': certificate_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/certificates')
def get_certificates():
    """API endpoint to get all certificates"""
    try:
        # In a real implementation, you would query the blockchain
        # For now, return mock data
        certificates = [
            {
                'id': 'cert_1',
                'studentName': 'John Doe',
                'courseName': 'Blockchain Development',
                'grade': 'A+',
                'date': '2024-01-15'
            }
        ]
        return jsonify({'success': True, 'certificates': certificates})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/verify-pdf', methods=['POST'])
def verify_pdf():
    """API endpoint to verify PDF certificate - exact same logic as your Streamlit verifier"""
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['pdf_file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        temp_file = "certificate.pdf"
        file.save(temp_file)
        
        try:
            # Extract data from the uploaded certificate using your existing function
            uid, candidate_name, course_name, org_name = extract_certificate(temp_file)
            
            # Display PDF using your existing function
            pdf_html = display_pdf_html(temp_file)
            os.remove(temp_file)

            original_data = {
                "uid": uid,
                "candidate_name": candidate_name,
                "course_name": course_name,
                "org_name": org_name
            }

            # Generate hash ID from the extracted certificate content - exact same logic
            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            # First, check if this cert ID exists on chain - exact same logic
            try:
                is_verified = contract.functions.isVerified(certificate_id).call()
            except Exception as e:
                print(f"Error checking verification status: {str(e)}")
                is_verified = False

            if is_verified:
                # Retrieve the certificate data from the blockchain - exact same logic
                try:
                    trusted_data_raw = contract.functions.getCertificate(certificate_id).call()
                    trusted_data = {
                        "uid": trusted_data_raw[0],
                        "candidate_name": trusted_data_raw[1],
                        "course_name": trusted_data_raw[2],
                        "org_name": trusted_data_raw[3]
                    }

                    # Check if UID matches between the uploaded and blockchain data
                    if original_data["uid"] == trusted_data["uid"]:
                        # Compare the other fields if UID matches - exact same logic
                        mismatched_fields = []
                        for key in original_data:
                            if original_data[key] != trusted_data.get(key, None):
                                mismatched_fields.append(f"{key}: Uploaded = {original_data[key]}, Blockchain = {trusted_data.get(key)}")

                        return jsonify({
                            'success': True,
                            'verified': True,
                            'pdfHtml': pdf_html,
                            'extractedData': original_data,
                            'mismatchedFields': mismatched_fields if mismatched_fields else None
                        })
                    else:
                        return jsonify({
                            'success': True,
                            'verified': False,
                            'pdfHtml': pdf_html,
                            'extractedData': original_data,
                            'error': 'UID does not match with blockchain record.'
                        })

                except Exception as e:
                    return jsonify({
                        'success': True,
                        'verified': False,
                        'pdfHtml': pdf_html,
                        'extractedData': original_data,
                        'error': f'Error retrieving certificate data from blockchain: {str(e)}'
                    })
            else:
                return jsonify({
                    'success': True,
                    'verified': False,
                    'pdfHtml': pdf_html,
                    'extractedData': original_data,
                    'error': 'Certificate not found on blockchain. It may be tampered or not issued.'
                })

        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return jsonify({'success': False, 'error': f'Error while processing certificate: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/verify-certificate-id', methods=['POST'])
def verify_certificate_id():
    """API endpoint to verify certificate by ID - exact same logic as your Streamlit verifier"""
    try:
        data = request.get_json()
        certificate_id = data.get('certificateId')
        
        try:
            # Use your existing view_certificate function
            pdf_html = view_certificate_flask(certificate_id)
            result = contract.functions.isVerified(certificate_id).call()
            
            if result:
                return jsonify({
                    'success': True, 
                    'pdfHtml': pdf_html
                })
            else:
                return jsonify({'success': False, 'error': 'Invalid Certificate ID!'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': 'Invalid Certificate ID!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/verify-certificate', methods=['POST'])
def verify_certificate():
    """API endpoint to verify a certificate"""
    try:
        data = request.get_json()
        certificate_id = data.get('certificateId')
        
        # In a real implementation, you would query the blockchain
        # For now, return mock verification
        if certificate_id == 'cert_1':
            certificate = {
                'studentName': 'John Doe',
                'courseName': 'Blockchain Development',
                'grade': 'A+',
                'date': '2024-01-15'
            }
            return jsonify({'success': True, 'certificate': certificate})
        else:
            return jsonify({'success': False, 'error': 'Certificate not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/blockchain-status')
def blockchain_status():
    """API endpoint to check blockchain connection status"""
    try:
        is_connected = w3.is_connected()
        return jsonify({
            'success': True,
            'connected': is_connected,
            'network_id': w3.net.version if is_connected else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 