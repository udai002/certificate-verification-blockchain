// Main JavaScript file for VeriSure application

// MetaMask connection function
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

// Role selection function
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

// Clear all messages
function clearMessages() {
    const messages = ['successMessage', 'errorMessage', 'warningMessage', 'infoMessage'];
    messages.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.style.display = 'none';
        }
    });
}

// Show message function
function showMessage(type, message) {
    clearMessages();
    const element = document.getElementById(type + 'Message');
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

// Form submission handler
function handleFormSubmit(formId, endpoint, successCallback = null) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        // Convert FormData to JSON
        const jsonData = {};
        for (let [key, value] of formData.entries()) {
            jsonData[key] = value;
        }
        
        fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showMessage('success', data.message || 'Operation successful!');
                if (successCallback) {
                    successCallback(data);
                }
            } else {
                showMessage('error', data.error || 'Operation failed!');
            }
        })
        .catch(error => {
            showMessage('error', 'Error: ' + error);
        });
    });
}

// Toggle form visibility
function toggleForm(selectId, form1Id, form2Id) {
    const select = document.getElementById(selectId);
    const form1 = document.getElementById(form1Id);
    const form2 = document.getElementById(form2Id);
    
    if (!select || !form1 || !form2) return;
    
    const value = select.value;
    
    if (value === form1Id.replace('Form', '')) {
        form1.style.display = 'block';
        form2.style.display = 'none';
    } else {
        form1.style.display = 'none';
        form2.style.display = 'block';
    }
    
    // Clear messages and PDF viewer
    clearMessages();
    const pdfViewer = document.getElementById('pdfViewer');
    if (pdfViewer) {
        pdfViewer.innerHTML = '';
    }
}

// Handle file upload
function handleFileUpload(fileInputId, endpoint, successCallback = null) {
    const fileInput = document.getElementById(fileInputId);
    if (!fileInput) return;

    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        
        if (file) {
            const formData = new FormData();
            formData.append('pdf_file', file);
            
            fetch(endpoint, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (successCallback) {
                        successCallback(data);
                    }
                } else {
                    showMessage('error', data.error || 'File processing failed!');
                }
            })
            .catch(error => {
                showMessage('error', 'Error processing file: ' + error);
            });
        }
    });
}

// Initialize page-specific functionality
function initializePage() {
    // Check if we're on the main page
    const roleCards = document.querySelectorAll('.role-card');
    if (roleCards.length > 0) {
        roleCards.forEach(card => {
            card.addEventListener('click', function() {
                const role = this.getAttribute('data-role');
                if (role) {
                    selectRole(role);
                }
            });
        });
    }
    
    // Check if we're on the login page
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        handleFormSubmit('loginForm', '/api/login', function(data) {
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1000);
        });
    }
    
    // Check if we're on the register page
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        handleFormSubmit('registerForm', '/api/register', function(data) {
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1000);
        });
    }
    
    // Check if we're on the institute dashboard
    const certForm = document.getElementById('certForm');
    if (certForm) {
        handleFormSubmit('certForm', '/api/generate-certificate', function(data) {
            showMessage('info', `Use this Certificate ID for verification: ${data.certificateId}`);
            certForm.reset();
        });
    }
    
    const viewCertForm = document.getElementById('viewCertForm');
    if (viewCertForm) {
        handleFormSubmit('viewCertForm', '/api/view-certificate', function(data) {
            const pdfViewer = document.getElementById('pdfViewer');
            if (pdfViewer && data.pdfHtml) {
                pdfViewer.innerHTML = data.pdfHtml;
            }
        });
    }
    
    // Check if we're on the verifier dashboard
    const verifyCertForm = document.getElementById('verifyCertForm');
    if (verifyCertForm) {
        handleFormSubmit('verifyCertForm', '/api/verify-certificate-id', function(data) {
            const pdfViewer = document.getElementById('pdfViewer');
            if (pdfViewer && data.pdfHtml) {
                pdfViewer.innerHTML = data.pdfHtml;
            }
        });
    }
    
    const pdfFileInput = document.getElementById('pdfFile');
    if (pdfFileInput) {
        handleFileUpload('pdfFile', '/api/verify-pdf', function(data) {
            const pdfViewer = document.getElementById('pdfViewer');
            if (pdfViewer && data.pdfHtml) {
                pdfViewer.innerHTML = data.pdfHtml;
            }
            
            if (data.verified) {
                showMessage('success', 'Certificate validated successfully and matches blockchain record.');
            } else {
                showMessage('error', 'Certificate not found on blockchain. It may be tampered or not issued.');
            }
            
            if (data.extractedData) {
                let infoText = 'Extracted values from uploaded certificate:';
                for (const [key, value] of Object.entries(data.extractedData)) {
                    infoText += `\n- ${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}`;
                }
                showMessage('info', infoText);
            }
            
            if (data.mismatchedFields && data.mismatchedFields.length > 0) {
                let warningText = 'The following fields have been modified or misplaced:';
                data.mismatchedFields.forEach(field => {
                    warningText += `\n- ${field}`;
                });
                showMessage('warning', warningText);
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePage); 