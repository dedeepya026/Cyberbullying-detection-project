import streamlit as st
import requests

st.set_page_config(page_title="Cyberbullying Detector", layout="centered")

# Title and instructions
st.title("🛡️ Cyberbullying Comment Detector")
st.write("Type a comment below to check whether it could be considered offensive or cyberbullying:")

# Text input
comment = st.text_area("💬 Enter your comment:")

# When user inputs something
if comment:
    payload = {"comment": comment}
    
    
    try:
        response = requests.post("http://127.0.0.1:5001/predict", json=payload)

        if response.status_code == 200:
            result = response.json()
            if result.get("is_offensive"):
                st.warning("⚠️ This comment may be considered offensive or cyberbullying.")
            else:
                st.success("✅ This comment seems appropriate.")
        else:
            # Handle known or unknown error response
            try:
                error_message = response.json().get("error", "Unknown error occurred.")
            except Exception:
                error_message = response.text or "No error message returned."
            st.error(f"🚫 API Error ({response.status_code}): {error_message}")

    except requests.exceptions.ConnectionError:
        st.error("🚫 Could not connect to the backend Flask API. Is it running?")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")
