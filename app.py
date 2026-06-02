import streamlit as st
import smtplib
import random
from email.message import EmailMessage

# Pink background aur White input boxes
st.markdown("""
    <style>
    .stApp { background-color: #FFC0CB; }
    .stTextInput > div > div > input { background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Session state initialize karein
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Agar login nahi hua, to Form dikhayein
if not st.session_state.logged_in:
    st.title("Welcome to My-Secure-Fashion")
    EMAIL_ADDRESS = "itscyberme@gmail.com"
    EMAIL_PASSWORD = "ritaxgheukirpdzr"

    def send_otp_email(user_email, otp):
        msg = EmailMessage()
        msg['Subject'] = 'Your Verification Code'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user_email
        msg.set_content(f"Aapka verification code hai: {otp}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password")

    if 'otp' not in st.session_state:
        st.session_state.otp = None

    if st.button("Send OTP"):
        st.session_state.otp = random.randint(100000, 999999)
        send_otp_email(email, st.session_state.otp)
        st.success("OTP sent!")

    user_otp = st.text_input("Enter OTP")
    if st.button("Verify"):
        if user_otp == str(st.session_state.otp):
            st.session_state.logged_in = True
            st.rerun() # Page refresh hoga
        else:
            st.error("Invalid OTP.")

# Agar login ho gaya, to asli store dikhayein
else:
    st.title("Fashion Product Showcase")
    st.write("Aap successfully login ho chuki hain! Yahan aapki collection hai.")
    # Yahan apna baaki ka shopping app ka code daal sakti hain
