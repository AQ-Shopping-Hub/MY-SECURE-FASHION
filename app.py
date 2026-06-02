import streamlit as st
import smtplib
import random
from email.message import EmailMessage

# CSS: Background Pink aur Input Boxes White
st.markdown("""
    <style>
    .stApp {
        background-color: #FFC0CB; /* Light Pink Background */
    }
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Welcome to My-Secure-Fashion")

# Yahan apna email aur wo 16-digit code daalein
EMAIL_ADDRESS = "your_email@gmail.com" 
EMAIL_PASSWORD = "rita xghe ukir pdzr" 

def send_otp_email(user_email, otp):
    msg = EmailMessage()
    msg['Subject'] = 'Your Verification Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email
    msg.set_content(f"Aapka verification code hai: {otp}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# Form fields
name = st.text_input("Enter your name")
email = st.text_input("Enter your email")
password = st.text_input("Enter your password", type="password")

if 'otp' not in st.session_state:
    st.session_state.otp = None

if st.button("Send OTP"):
    if name and email and password:
        st.session_state.otp = random.randint(100000, 999999)
        send_otp_email(email, st.session_state.otp)
        st.success("OTP sent to your email!")
    else:
        st.error("Please fill all the fields!")

user_otp = st.text_input("Enter OTP received on email")
if st.button("Verify"):
    if user_otp == str(st.session_state.otp):
        st.success(f"Welcome {name}! Verification successful.")
    else:
        st.error("Invalid OTP.")
