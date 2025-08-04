# VeriSure - Flask Application

This directory now contains both **Streamlit** and **Flask** versions of the VeriSure blockchain certification application. Your existing Streamlit code remains completely unchanged and functional.

## 🚀 Quick Start

### Option 1: Run Flask Application Only
```bash
cd application
python run_flask.py
```
Flask app will be available at: http://localhost:5000

### Option 2: Run Streamlit Application Only
```bash
cd application
streamlit run app.py
```
Streamlit app will be available at: http://localhost:8501

### Option 3: Run Both Applications Simultaneously
Open two terminal windows:

**Terminal 1 (Flask):**
```bash
cd application
python run_flask.py
```

**Terminal 2 (Streamlit):**
```bash
cd application
streamlit run app.py
```

## 📋 Prerequisites

### For Flask Application
```bash
pip install -r requirements_flask.txt
```

### For Streamlit Application
Your existing dependencies remain the same.

### Blockchain Setup
1. Make sure Ganache is running on http://127.0.0.1:7545
2. Deploy your smart contracts using Truffle
3. Ensure `deployment_config.json` contains the correct contract addresses

## 🔧 Flask Application Features

### Web Interface
- **Main Page**: Role selection (Institute/Verifier) with MetaMask integration
- **Login Page**: User authentication
- **Institute Dashboard**: Issue and manage certificates
- **Verifier Dashboard**: Verify certificates

### REST API Endpoints
- `GET /` - Main page
- `POST /api/set-role` - Set user role
- `POST /api/login` - User authentication
- `POST /api/issue-certificate` - Issue new certificate
- `GET /api/certificates` - Get all certificates
- `POST /api/verify-certificate` - Verify certificate
- `GET /api/blockchain-status` - Check blockchain connection

### Static Assets
- `GET /logo` - Serve main logo GIF
- `GET /institute-logo` - Serve institute logo
- `GET /verifier-logo` - Serve verifier logo

## 🏗️ Architecture

### File Structure
```
application/
├── app.py                    # Original Streamlit app (unchanged)
├── flask_app.py             # New Flask application
├── run_flask.py             # Flask application runner
├── requirements_flask.txt   # Flask dependencies
├── connection.py            # Shared blockchain connection
├── pages/                   # Streamlit pages (unchanged)
├── utils/                   # Streamlit utilities (unchanged)
└── assets/                  # Shared assets
```

### Key Features
- **Shared Blockchain Connection**: Both apps use the same `connection.py`
- **Independent Operation**: Apps can run simultaneously on different ports
- **Same Functionality**: Both apps provide the same core features
- **No Code Changes**: Your existing Streamlit code remains untouched

## 🔄 Integration with Smart Contracts

The Flask application uses the same smart contract integration as your Streamlit app:

```python
from connection import w3, contract, contract_abi
```

### Blockchain Operations
- **Certificate Issuance**: Calls smart contract to issue certificates
- **Certificate Verification**: Queries blockchain for certificate validation
- **MetaMask Integration**: Web3 wallet connection for transactions

## 🎨 UI/UX Features

### Responsive Design
- Modern, clean interface
- Mobile-friendly layout
- Consistent styling with your brand

### Interactive Elements
- Role selection cards with hover effects
- Real-time MetaMask connection status
- Dynamic certificate management
- Instant verification results

## 🛠️ Development

### Adding New Features
1. **Flask Routes**: Add new routes in `flask_app.py`
2. **API Endpoints**: Create new API endpoints for functionality
3. **Frontend**: Update HTML templates or add JavaScript
4. **Smart Contracts**: Extend blockchain functionality

### Testing
```bash
# Test Flask API endpoints
curl http://localhost:5000/api/blockchain-status

# Test certificate issuance
curl -X POST http://localhost:5000/api/issue-certificate \
  -H "Content-Type: application/json" \
  -d '{"studentName":"John Doe","courseName":"Blockchain","grade":"A+","date":"2024-01-15"}'
```

## 🔒 Security Considerations

### Current Implementation
- Basic session management using IP addresses
- Simple authentication (should be enhanced for production)
- CORS enabled for cross-origin requests

### Production Recommendations
- Implement proper session management (Flask-Session)
- Add database authentication
- Use HTTPS in production
- Implement rate limiting
- Add input validation and sanitization

## 🚀 Deployment

### Local Development
```bash
python run_flask.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app

# Using Docker (create Dockerfile)
docker build -t verisure-flask .
docker run -p 5000:5000 verisure-flask
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:5000/api/blockchain-status
```

### Logs
Flask debug mode provides detailed logs for development.

## 🤝 Contributing

When adding new features:
1. Keep both Streamlit and Flask versions in sync
2. Test both applications thoroughly
3. Update this README with new features
4. Maintain backward compatibility

## 📞 Support

If you encounter issues:
1. Check blockchain connection status
2. Verify all dependencies are installed
3. Ensure Ganache is running
4. Check console logs for error messages

---

**Note**: Your existing Streamlit application remains completely functional and unchanged. The Flask application is an additional interface that provides the same functionality through a web-based REST API. 