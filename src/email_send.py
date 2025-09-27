import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

# --- SESSION STATE ---
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False
if "confirmed_send" not in st.session_state:
    st.session_state.confirmed_send = None

# --- DIALOG ---
@st.dialog("contact @arm", dismissible = False)
def send_dialog():
    st.write("Are you sure you want to send this email?")
    col1, col2 = st.columns(2)
    with col2:
        if st.button("✅ Yes"):
            st.session_state.confirmed_send = True
            st.session_state.show_dialog = False
            st.rerun()
    with col1:
        if st.button("❌ No"):
            st.session_state.confirmed_send = False
            st.session_state.show_dialog = False
            st.rerun()

def send_email(message):
    # Step 1: Show dialog first
    st.session_state.show_dialog = True
    st.session_state.message_to_send = message
    st.rerun()



def smtp_send():
    
    try:
        message = st.session_state.message_to_send
        smtp_server = st.secrets["smtp_server"]
        smtp_port = st.secrets["smtp_port"]
        email_user = st.secrets["email_user"]
        email_pass = st.secrets["email_pass"]
        email_destination = st.secrets["email_destination"]

        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = email_destination
        msg["Subject"] = message["subject"]
        msg["Reply-To"] = message["sender"]
        body = f"Sender: {message['sender']}\n\n{message['body']}"
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(message["sender"], email_destination, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)
    finally:
        st.session_state.confirmed_send = None


