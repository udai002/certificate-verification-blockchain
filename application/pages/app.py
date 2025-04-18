import streamlit as st
from PIL import Image
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

from streamlit.components.v1 import html

js_code = """
<script>
    async function connectMetaMask() {
        if (window.ethereum) {
            try {
                await window.ethereum.request({ method: 'eth_requestAccounts' });
                const account = window.ethereum.selectedAddress;
                document.getElementById('wallet').textContent = account;
            } catch (error) {
                console.error(error);
                alert('Connection failed.');
            }
        } else {
            alert('MetaMask not installed!');
        }
    }
</script>
<button onclick="connectMetaMask()">Connect MetaMask</button>
<p id="wallet">Not connected</p>
"""
html(js_code)

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()




col1,col2,col3 =st.columns([1,2,1])
with col2:
    st.image(".assets/MyLogo3.gif",caption="",use_column_width=False,width=300)

st.title("VeriFicate")
st.write("")
st.subheader("Select Your Role")

col1, col2 = st.columns(2)
institite_logo = Image.open("../assets/institute_logo.png")
with col1:
    st.image(institite_logo, output_format="jpg", width=230)
    clicked_institute = st.button("Institute")

company_logo = Image.open("../assets/company_logo.jpg")
with col2:
    st.image(company_logo, output_format="jpg", width=230)
    clicked_verifier = st.button("Verifier")

if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')
