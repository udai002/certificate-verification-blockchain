# VeriSure - Blockchain Certificate Verification System

A comprehensive blockchain-based certificate verification system with separate testing (Streamlit) and deployment (Flask) environments.

## Project Structure

```
pursuit/
├── streamlit_app/          # Streamlit application for testing
│   ├── app.py             # Main Streamlit app
│   ├── pages/             # Streamlit pages
│   ├── utils/             # Utility functions
│   ├── db/                # Database connections
│   ├── assets/            # Static assets
│   └── requirements.txt   # Python dependencies
├── flask_app/             # Flask application for deployment
│   ├── app.py             # Main Flask app
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   ├── utils/             # Utility functions
│   ├── db/                # Database connections
│   ├── api/               # API endpoints
│   └── requirements.txt   # Python dependencies
├── contracts/             # Smart contracts
├── migrations/            # Database migrations
├── assets/                # Shared assets
└── docs/                  # Documentation
```

## Features

- **Blockchain Integration**: Smart contract-based certificate storage and verification
- **Dual Interface**: Streamlit for testing, Flask for production deployment
- **Certificate Generation**: Create and issue certificates on blockchain
- **Certificate Verification**: Verify certificates using PDF upload or certificate ID
- **User Authentication**: Firebase-based authentication system
- **IPFS Storage**: Pinata IPFS integration for certificate storage

## Quick Start

### Streamlit (Testing Environment)
```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

### Flask (Production Environment)
```bash
cd flask_app
pip install -r requirements.txt
python app.py
```

## Smart Contract Deployment

```bash
truffle migrate --reset
```

## Environment Variables

Create `.env` files in both `streamlit_app/` and `flask_app/` directories:

```
PINATA_API_KEY=your_pinata_api_key
PINATA_API_SECRET=your_pinata_secret_key
institute_email=your_institute_email
institute_password=your_institute_password
```

## License

MIT License

