# streamlit_app.py
import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🚀",
    layout="centered",
)

# --- App Title ---
st.title("🚀 My Public Streamlit App")
st.markdown("Welcome! This app is deployed publicly using **Streamlit Cloud**.")

# --- Sidebar ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "About"])

# --- Main Content ---
if page == "Home":
    st.subheader("🏠 Home Page")
    st.write("This is your main app area. You can add widgets and logic here.")

    # Example input/output
    name = st.text_input("Enter your name:")
    if st.button("Greet Me"):
        st.success(f"Hello, {name or 'friend'}! 👋")

elif page == "About":
    st.subheader("ℹ️ About")
    st.write("""
    This demo app is built with [Streamlit](https://streamlit.io).
    To deploy publicly:
    1. Push this file (`streamlit_app.py`) to a public GitHub repo.
    2. Go to [share.streamlit.io](https://share.streamlit.io).
    3. Connect your repo and deploy!
    """)

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")

