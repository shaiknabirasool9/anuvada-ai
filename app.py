import time
import streamlit as st
from google import genai

st.set_page_config(page_title="Anuvada AI", page_icon="🌐")

# Initialize the Gemini client using your secret
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Configuration Error: Check your secrets.toml file. Details: {e}")
    st.stop()

# System prompt configured for Hindi, Telugu, and clean English
SYSTEM_INSTRUCTION = """You are a Gen AI trainer. For any English text the user gives, reply in exactly this format:
**Hindi:** <Hindi translation>
**Telugu:** <Telugu translation>
**English (clean):** <corrected/improved English>
**Gen AI tip:** <one short tip, only if relevant>"""

st.title("🌐 Anuvada AI")
st.caption("English → Hindi + Telugu + English | Gen AI Trainer (Powered by Gemini)")

if "history" not in st.session_state:
    st.session_state.history = []

text = st.text_area("Enter English text", height=120)

if st.button("Convert") and text.strip():
    with st.spinner("Translating... Please wait..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=text,
                config={
                    'system_instruction': SYSTEM_INSTRUCTION,
                }
            )
            
            if response and response.text:
                result = response.text
                st.session_state.history.insert(0, (text, result))
                st.rerun()
            else:
                st.warning("Received an empty response from Gemini. Try again.")
                
        except Exception as e:
            st.error(f"API Error: {e}")

# Display history
for src, out in st.session_state.history:
    with st.expander(f"📝 {src[:50]}..."):
        st.markdown(out)