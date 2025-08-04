# VeriSure - Blockchain Certificate Verification System

A comprehensive blockchain-based certificate verification system with separate testing (Streamlit) and deployment (Flask) environments.
```

## Features

- **Blockchain Integration**: Smart contract-based certificate storage and verification
- **Certificate Generation**: Create and issue certificates on blockchain
- **Certificate Verification**: Verify certificates using PDF upload or certificate ID
- **User Authentication**: Firebase-based authentication system
- **IPFS Storage**: Pinata IPFS integration for certificate storage

## Quick Start


## Smart Contract Deployment

```bash
truffle migrate --reset
```

## Environment Variables

```
PINATA_API_KEY=your_pinata_api_key
PINATA_API_SECRET=your_pinata_secret_key
institute_email=your_institute_email
institute_password=your_institute_password
```

## License

MIT License

