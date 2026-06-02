import streamlit as st
import smtplib
import random
from email.message import EmailMessage

# --- CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #FFC0CB; }
    .stTextInput > div > div > input { background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- PART 1: LOGIN PAGE ---
if not st.session_state.logged_in:
    st.title("Welcome to My-Secure-Fashion")
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password")

    if 'otp' not in st.session_state: st.session_state.otp = None

    if st.button("Send OTP"):
        st.session_state.otp = random.randint(100000, 999999)
        # Email sending logic...
        st.success("OTP sent!")

    user_otp = st.text_input("Enter OTP")
    if st.button("Verify"):
        if user_otp == str(st.session_state.otp):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid OTP.")

# --- PART 2: SHOPPING PAGE (After Login) ---
else:
    st.title("🛍️ My-Secure-Fashion Collection")
    
    # Example Product
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Silk Dress")
        st.write("Price: Rs. 5000")
    with col2:
        st.write("Description: Stylish Pink Silk")
        # WhatsApp Link (Apna number yahan daalein)
        st.link_button("Order on WhatsApp", "https://wa.me/923706447456")
    
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()
