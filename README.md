                                                             **VerifyLab**
                                                             
This project provides a Blockchain based solution for generating and verifying digital certificates. The certificate information (uid, candidate_name, course_name, org_name, ipfs_hash) is stored on the blockchain. First, the certificate pdf is generated and stored onto IPFS using Pinata service. Then, the IPFS hash obtained is stored on the blockchain along with other information.


The system categorized in to two entities:
- **Institute**: Responsible for generating and issuing certificates. Has the functionality to generate and view certificates.

- **Verifier**: Responsible for verifying certificates. Has the functionality to verify certificates by either uploading a certificate pdf or by inputting the certificate id.

## Key Terminologies

- **Smart Contract:** Utilizes a Solidity smart contract to manage and store certificate details on the Ethereum blockchain.
- **IPFS Integration:** Stores certificate PDFs on IPFS via Pinata for decentralized and secure file storage.
- **Firebase Authentication:** Uses Firebase for authentication.
- **Streamlit App:** Provides a user-friendly interface for generating and verifying certificates.

