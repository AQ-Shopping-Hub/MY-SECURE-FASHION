import streamlit as st
import smtplib
import random
from email.message import EmailMessage

st.title("Welcome to My-Secure-Fashion")

# Email aur Password yahan dalen
EMAIL_ADDRESS = "your_email@gmail.com"  # Apna email likhein
EMAIL_PASSWORD = "ritaxgheukirpdzr"    # Ye wahi 16-digit code hai jo file 1000249648.jpg mein hai

def send_otp_email(user_email, otp):
    msg = EmailMessage()
    msg['Subject'] = 'Your Verification Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email
    msg.set_content(f"Aapka verification code hai: {otp}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

email = st.text_input("Enter your email for sign up")

if 'otp' not in st.session_state:
    st.session_state.otp = None

if st.button("Send OTP"):
    st.session_state.otp = random.randint(100000, 999999)
    send_otp_email(email, st.session_state.otp)
    st.success("OTP sent to your email!")

user_otp = st.text_input("Enter OTP received on email")
if st.button("Verify"):
    if user_otp == str(st.session_state.otp):
        st.success("Verification successful! You can now access the shop.")
    else:
        st.error("Invalid OTP. Please try again.")
