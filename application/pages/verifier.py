import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate
from connection import contract
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
sideb = st.sidebar
check1 = sideb.button("Logout")
if check1:
    switch_page('app')
hide_icons()
hide_sidebar()
remove_whitespaces()

options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)

        try:
            # Extract data from the uploaded certificate
            uid, candidate_name, course_name, org_name = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            original_data = {
                "uid": uid,
                "candidate_name": candidate_name,
                "course_name": course_name,
                "org_name": org_name
            }

            # Generate hash ID from the extracted certificate content
            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            # First, check if this cert ID exists on chain
            try:
                is_verified = contract.functions.isVerified(certificate_id).call()
            except Exception as e:
                st.write(f"Error checking verification status: {str(e)}")
                is_verified = False

            if is_verified:
                st.success("Certificate hash found on blockchain.")

                # Retrieve the certificate data from the blockchain
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
                        st.success("UID matches with blockchain record.")

                        # Compare the other fields if UID matches
                        mismatched_fields = []
                        for key in original_data:
                            if original_data[key] != trusted_data.get(key, None):
                                mismatched_fields.append(f"{key}: Uploaded = {original_data[key]}, Blockchain = {trusted_data.get(key)}")

                        # If there are mismatches, show them
                        if mismatched_fields:
                            st.warning("The following fields have been modified or misplaced:")
                            for mismatch in mismatched_fields:
                                st.markdown(f"- {mismatch}")
                        else:
                            st.success("Certificate validated successfully and matches blockchain record.")
                    else:
                        st.error("UID does not match with blockchain record.")

                except Exception as e:
                    st.write(f"Error retrieving certificate data from blockchain: {str(e)}")
                    trusted_data = {}

            else:
                st.error("Certificate not found on blockchain. It may be tampered or not issued.")
                st.info("Extracted values from uploaded certificate:")
                for k, v in original_data.items():
                    st.markdown(f"- **{k.capitalize()}**: `{v}`")

        except Exception as e:
            st.error(f"Error while processing certificate: {str(e)}")

elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Validate")
    if submit:
        try:
            view_certificate(certificate_id)
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate validated successfully!")
            else:
                st.error("Invalid Certificate ID!")
        except Exception as e:
            st.error("Invalid Certificate ID!")
