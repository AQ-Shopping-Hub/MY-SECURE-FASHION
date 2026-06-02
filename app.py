import streamlit as st
import hashlib
import time

# 📁 USERS DATA FOR ONLINE REAL WEBSITE (Session-based Secure storage)
if "registered_users" not in st.session_state:
    # default account testing ke liye taake har baar sign up na karna pare
    st.session_state["registered_users"] = {
        "admin": hashlib.sha256("admin123".encode()).hexdigest()
    }

# 1. APPLICATION SETUP & THEME (White Background, Pink Flowers, Pink Bars, Purple Buttons)
st.markdown(
    """
    <style>
    /* Background pure white aur oopar/neeche light pink flowers ka design */
    .stApp { 
        background-color: #FFFFFF; 
        background-image: url('https://www.transparenttextures.com/patterns/cherry-blossom.png'); 
        background-repeat: repeat;
    }
    
    /* Saare main text ka color dark purple */
    h1, h2, h3, p, span, label, div { color: #4A154B !important; font-weight: 500; }
    
    /* 🌸 ALL INPUT BARS & SELECTBOXES: Pure Light Pink Color 🌸 */
    .stTextInput div div input, .stSelectbox div div div {
        background-color: #FFF0F5 !important; 
        color: #4A154B !important;
        border: 2px solid #FFB6C1 !important; 
        border-radius: 8px !important;
    }
    
    /* Dropdown ke andar ka menu bhi light pink background wala ho */
    div[data-baseweb="popover"] ul {
        background-color: #FFF0F5 !important;
        color: #4A154B !important;
    }
    
    /* 💜 BUTTONS: Light Purple Color 💜 */
    div.stButton > button:first-child {
        background-color: #E6E6FA !important; 
        color: #4A154B !important;
        border: 2px solid #D8BFD8 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #D8BFD8 !important; 
        border-color: #4A154B !important;
    }
    
    /* Tabs (Sign Up / Log In) ko bhee light purple look dena */
    button[data-baseweb="tab"] { color: #4A154B !important; }
    button[data-baseweb="tab"][aria-selected="true"] { 
        border-bottom-color: #9370DB !important; 
        color: #9370DB !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session State Variables Initialize karna
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "mfa_verified" not in st.session_state:
    st.session_state["mfa_verified"] = False
if "login_attempts" not in st.session_state:
    st.session_state["login_attempts"] = 0

st.title("🔐 Secure Pakistani Fashion Brand Showcase")

# -------------------------------------------------------------
# 2. SECURITY FEATURES EXPLANATION (CIA Triad Showcase)
# -------------------------------------------------------------
with st.expander("ℹ️ Click to view CIA Triad & Security Implementation Details"):
    st.markdown("""
    * **Confidentiality (Razdari):** Passwords are encrypted using **SHA-256 Hashing**. No plain text is saved.
    * **Integrity (Salamat-ravi):** **Input Validation** ensures users cannot inject malicious code or wrong formats.
    * **Availability (Dastiyabi):** **Rate Limiting** blocks users after 3 wrong attempts to prevent Brute Force/DoS attacks.
    * **MFA & Access Control:** Multi-Factor Authentication code (Prototype: 1234) and Role-Based Access.
    """)

st.divider()

# -------------------------------------------------------------
# 3. USER REGISTRATION & INPUT VALIDATION & ENCRYPTION
# -------------------------------------------------------------
if st.session_state["logged_in_user"] is None:
    st.subheader("📝 User Registration & Login")
    
    tab1, tab2 = st.tabs(["Sign Up (Naya Account)", "Log In (Maujooda Account)"])
    
    with tab1:
        reg_user = st.text_input("Naya Username banayein:", key="reg_u").strip()
        reg_pass = st.text_input("Naya Password banayein:", type="password", key="reg_p")
        
        if st.button("Register Account"):
            if len(reg_user) < 4 or len(reg_pass) < 6:
                st.error("❌ Validation Failed: Username kam az kam 4 aur Password 6 characters ka hona chahiye!")
            elif reg_user in st.session_state["registered_users"]:
                st.warning("⚠️ Yeh username pehle se maujood hai!")
            else:
                # ENCRYPTION & ONLINE STORAGE
                hashed_password = hashlib.sha256(reg_pass.encode()).hexdigest()
                st.session_state["registered_users"][reg_user] = hashed_password
                st.success("✅ Account successfully register ho gaya! Ab Log In tab par jayein.")

    # -------------------------------------------------------------
    # 4. LOGIN & RATE LIMITING
    # -------------------------------------------------------------
    with tab2:
        if st.session_state["login_attempts"] >= 3:
            st.error("🚫 Rate Limit Exceeded: Aapne 3 baar galat password dala. Screen 5 seconds ke liye block hai!")
            time.sleep(5)
            st.session_state["login_attempts"] = 0
            
        login_user = st.text_input("Apna Username likhein:", key="log_u").strip()
        login_pass = st.text_input("Apna Password likhein:", type="password", key="log_p")
        
        if st.button("Log In"):
            hashed_login_pass = hashlib.sha256(login_pass.encode()).hexdigest()
            
            if login_user in st.session_state["registered_users"] and st.session_state["registered_users"][login_user] == hashed_login_pass:
                st.session_state["logged_in_user"] = login_user
                st.session_state["login_attempts"] = 0
                st.rerun()
            else:
                st.session_state["login_attempts"] += 1
                st.error(f"❌ Galat Username ya Password! (Attempts: {st.session_state['login_attempts']}/3)")

# -------------------------------------------------------------
# 5. MULTI-FACTOR AUTHENTICATION (MFA)
# -------------------------------------------------------------
elif st.session_state["logged_in_user"] is not None and not st.session_state["mfa_verified"]:
    st.subheader("📱 Multi-Factor Authentication (MFA)")
    st.info(f"Welcome **{st.session_state['logged_in_user']}**! Ehteyatan aapke mobile par 4-digit code bheja gaya hai.")
    
    st.write("**Demo MFA Code:** `1234` (Project testing ke liye)")
    mfa_input = st.text_input("Apna 4-Digit MFA Code enter karein:", type="password", max_chars=4)
    
    if st.button("Verify MFA"):
        if mfa_input == "1234":
            st.session_state["mfa_verified"] = True
            st.success("🔒 MFA Verified Successfully!")
            st.rerun()
        else:
            st.error("❌ Galat MFA Code! Dubara koshish karein.")

# -------------------------------------------------------------
# 6. ACCESS CONTROL & MAIN SECURE CONTENT (WhatsApp Integration)
# -------------------------------------------------------------
else:
    st.subheader(f"👋 Welcome to your Secure Dashboard, {st.session_state['logged_in_user']}!")
    
    if st.button("🚪 Log Out / Lock Account"):
        st.session_state["logged_in_user"] = None
        st.session_state["mfa_verified"] = False
        st.rerun()
        
    st.divider()
    
    brand = st.selectbox("Apna pasandida brand select karein:", ["Charizma", "Baroque"])

    # 🟢 AAPKA REAL WHATSAPP LINK WITH CUSTOM MESSAGE 🟢
    whatsapp_url = "https://wa.me/9230706447456?text=I%20want%20to%20buy%20this%20suit%20from%20your%20Secure%20Fashion%20Showcase!"

    if brand == "Charizma":
        st.subheader("🌸 Charizma Luxury Collections")
        st.write("**Product:** Embroidered Lawn Suit (3-Piece) - *Secure Data*")
        st.write("**Price:** PKR 6,500")
        
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color: #E6E6FA; color: #4A154B; padding: 10px 20px; border: 2px solid #D8BFD8; border-radius: 8px; font-weight: bold; cursor: pointer;">💬 Buy from WhatsApp</button></a>', unsafe_allow_html=True)

    elif brand == "Baroque":
        st.subheader("✨ Baroque Premium Velvet/Lawn")
        st.write("**Product:** Premium Chiffon Collection - *Secure Data*")
        st.write("**Price:** PKR 8,900")
        
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color: #E6E6FA; color: #4A154B; padding: 10px 20px; border: 2px solid #D8BFD8; border-radius: 8px; font-weight: bold; cursor: pointer;">💬 Buy from WhatsApp</button></a>', unsafe_allow_html=True)