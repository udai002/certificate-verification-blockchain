// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Certification {
    struct Certificate {
        string uid;
        string candidate_name;
        string course_name;
        string org_name;
        string ipfs_hash;
        bool isRevoked; // New flag to track if certificate is revoked
    }

    address public issuer;

    constructor() {
        issuer = msg.sender;
    }

    modifier onlyIssuer() {
        require(msg.sender == issuer, "Only issuer can perform this action");
        _;
    }

    mapping(string => Certificate) public certificates;
    event CertificateGenerated(string certificate_id);
    event CertificateRevoked(string certificate_id);
    event CertificateUpdated(string certificate_id);

    // Function to generate and store certificates
    function generateCertificate(
        string memory _certificate_id,
        string memory _uid,
        string memory _candidate_name,
        string memory _course_name,
        string memory _org_name,
        string memory _ipfs_hash
    ) public onlyIssuer {
        require(
            bytes(certificates[_certificate_id].ipfs_hash).length == 0,
            "Certificate with this ID already exists"
        );

        Certificate memory cert = Certificate({
            uid: _uid,
            candidate_name: _candidate_name,
            course_name: _course_name,
            org_name: _org_name,
            ipfs_hash: _ipfs_hash,
            isRevoked: false // Initially not revoked
        });

        certificates[_certificate_id] = cert;
        emit CertificateGenerated(_certificate_id);
    }

    // Function to revoke a certificate
    function revokeCertificate(string memory _certificate_id) public onlyIssuer {
        Certificate storage cert = certificates[_certificate_id];
        require(bytes(cert.ipfs_hash).length != 0, "Certificate does not exist");
        require(!cert.isRevoked, "Certificate already revoked");

        cert.isRevoked = true; // Mark the certificate as revoked
        emit CertificateRevoked(_certificate_id);
    }

    // Function to check if a certificate is revoked
    function isRevoked(string memory _certificate_id) public view returns (bool) {
        Certificate memory cert = certificates[_certificate_id];
        require(bytes(cert.ipfs_hash).length != 0, "Certificate does not exist");
        return cert.isRevoked;
    }

    // Function to update a certificate's details
    function updateCertificate(
        string memory _certificate_id,
        string memory _uid,
        string memory _candidate_name,
        string memory _course_name,
        string memory _org_name,
        string memory _ipfs_hash
    ) public onlyIssuer {
        Certificate storage cert = certificates[_certificate_id];
        require(bytes(cert.ipfs_hash).length != 0, "Certificate does not exist");
        require(!cert.isRevoked, "Certificate is revoked and cannot be updated");

        cert.uid = _uid;
        cert.candidate_name = _candidate_name;
        cert.course_name = _course_name;
        cert.org_name = _org_name;
        cert.ipfs_hash = _ipfs_hash;

        emit CertificateUpdated(_certificate_id);
    }

    // Function to get certificate details from blockchain by certificate ID
    function getCertificate(
        string memory _certificate_id
    )
        public
        view
        returns (
            string memory _uid,
            string memory _candidate_name,
            string memory _course_name,
            string memory _org_name,
            string memory _ipfs_hash,
            bool _isRevoked
        )
    {
        Certificate memory cert = certificates[_certificate_id];
        require(
            bytes(cert.ipfs_hash).length != 0,
            "Certificate with this ID does not exist"
        );

        return (
            cert.uid,
            cert.candidate_name,
            cert.course_name,
            cert.org_name,
            cert.ipfs_hash,
            cert.isRevoked
        );
    }

    // Function to check if a certificate ID exists on the blockchain
    function isVerified(string memory _certificate_id) public view returns (bool) {
        return bytes(certificates[_certificate_id].ipfs_hash).length != 0;
    }

    // Function to compare uploaded certificate data with blockchain stored data
    function compareCertificateData(
        string memory _certificate_id,
        string memory _uid,
        string memory _candidate_name,
        string memory _course_name,
        string memory _org_name
    ) public view returns (string memory) {
        Certificate memory cert = certificates[_certificate_id];
        require(
            bytes(cert.ipfs_hash).length != 0,
            "Certificate with this ID does not exist"
        );

        // Compare each field and return mismatch information
        string memory mismatchReport = "Certificate Data Mismatch Report:\n";
        
        if (keccak256(abi.encodePacked(cert.uid)) != keccak256(abi.encodePacked(_uid))) {
            mismatchReport = string(abi.encodePacked(mismatchReport, "- UID mismatch\n"));
        }
        if (keccak256(abi.encodePacked(cert.candidate_name)) != keccak256(abi.encodePacked(_candidate_name))) {
            mismatchReport = string(abi.encodePacked(mismatchReport, "- Candidate Name mismatch\n"));
        }
        if (keccak256(abi.encodePacked(cert.course_name)) != keccak256(abi.encodePacked(_course_name))) {
            mismatchReport = string(abi.encodePacked(mismatchReport, "- Course Name mismatch\n"));
        }
        if (keccak256(abi.encodePacked(cert.org_name)) != keccak256(abi.encodePacked(_org_name))) {
            mismatchReport = string(abi.encodePacked(mismatchReport, "- Organization Name mismatch\n"));
        }

        // If all fields match, we return a success message
        if (keccak256(abi.encodePacked(mismatchReport)) == keccak256("Certificate Data Mismatch Report:\n")) {
            return "Certificate data matches the blockchain record.";
        }

        return mismatchReport;
    }
}
