import streamlit as st
import random
import smtplib
from email.message import EmailMessage

# --- CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #FFC0CB; }
    .stTextInput > div > div > input { background-color: light purple !important; }
    </style>
    """, unsafe_allow_html=True)

# Email details
EMAIL_ADDRESS = "itscyberme@gmail.com"
EMAIL_PASSWORD = "ritaxgheukirpdzr"

# Session State Initialize
if 'page' not in st.session_state: st.session_state.page = "Sign-Up"
if 'otp' not in st.session_state: st.session_state.otp = None

# --- PAGE 1: SIGN-UP ---
if st.session_state.page == "Sign-Up":
    st.title("Sign-Up")
    st.text_input("Name")
    st.text_input("Email")
    st.text_input("Password", type="password")
    if st.button("Sign Up"):
        st.session_state.page = "Login"
        st.rerun()

# --- PAGE 2: LOGIN ---
elif st.session_state.page == "Login":
    st.title("Login")
    email = st.text_input("Enter Email")
    st.text_input("Enter Password", type="password")
    if st.button("Send OTP"):
        st.session_state.otp = random.randint(100000, 999999)
        # Email logic
        msg = EmailMessage()
        msg['Subject'] = 'Your OTP'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg.set_content(f"Aapka OTP code hai: {st.session_state.otp}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        st.session_state.page = "OTP"
        st.rerun()

# --- PAGE 3: OTP VERIFICATION ---
elif st.session_state.page == "OTP":
    st.title("Enter OTP")
    user_otp = st.text_input("Enter the code sent to your email")
    if st.button("Verify"):
        if user_otp == str(st.session_state.otp):
            st.session_state.page = "Final"
            st.rerun()
        else:
            st.error("Invalid OTP!")
# --- PAGE 4: FINAL SHOPPING PAGE (Product Showcase) ---
elif st.session_state.page == "Final":
    st.title("🛍️ My-Secure-Fashion Collection")
    st.write("Welcome! Aap successfully login aur verify ho chuki hain.")
    
    # Product 1
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Luxury Silk Suit")
        st.write("Price: Rs. 6,500")
    with col2:
        st.image("https://via.placeholder.com/150", caption="Silk Suit") # Yahan aap apni image ka link dal sakti hain
        st.link_button("Order on WhatsApp", "https://wa.me/923706447456") # Apna number likhein

    st.markdown("---")
    
    # Product 2
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Embroidered Lawn")
        st.write("Price: Rs. 4,200")
    with col4:
        st.link_button("Order on WhatsApp", "https://wa.me/923XXXXXXXXX")
    
    if st.button("Logout"):
        st.session_state.page = "Sign-Up"
        st.rerun()
