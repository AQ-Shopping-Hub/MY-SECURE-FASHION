import streamlit as st
import smtplib
import random
from email.message import EmailMessage

# Pink background aur White input boxes ke liye CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #FFC0CB; 
    }
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Welcome to My-Secure-Fashion")

# --- APNI DETAILS YAHAN LIKHEIN ---
EMAIL_ADDRESS = "itscyberme@gmail.com"  # Apna email
EMAIL_PASSWORD = "ritaxgheukirpdzr"    # Aapka 16-digit code (koi space nahi)

def send_otp_email(user_email, otp):
    msg = EmailMessage()
    msg['Subject'] = 'Your Verification Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email
    msg.set_content(f"Aapka verification code hai: {otp}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# User Input Fields
name = st.text_input("Enter your name")
email = st.text_input("Enter your email")
password = st.text_input("Enter your password") # type="password" hata diya taake nazar aaye

if 'otp' not in st.session_state:
    st.session_state.otp = None

if st.button("Send OTP"):
    if name and email and password:
        try:
            st.session_state.otp = random.randint(100000, 999999)
            send_otp_email(email, st.session_state.otp)
            st.success("OTP sent to your email!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please fill all the fields!")

user_otp = st.text_input("Enter OTP received on email")
if st.button("Verify"):
    if user_otp == str(st.session_state.otp) and st.session_state.otp is not None:
        st.success(f"Welcome {name}! Verification successful.")
    else:
        st.error("Invalid OTP or error occurred.")
