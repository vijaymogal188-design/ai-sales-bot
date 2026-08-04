import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Google Gemini Style", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# World-Class Google Gemini Style UI with #0B1020 Dark Gradient & Centered Prompt Box
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0B1020 !important;
        color: #F8FAFC !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 20%, #1e1b4b 0%, #0B1020 70%) !important;
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    /* Gemini Style Top Navbar */
    .gemini-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        background: transparent;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        z-index: 100;
    }
    .gemini-logo {
        font-size: 20px;
        font-weight: 800;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .gemini-nav-links {
        display: flex;
        gap: 24px;
        font-size: 14px;
        font-weight: 500;
        color: #94A3B8;
    }

    /* Gemini Hero Screen */
    .gemini-hero {
        min-height: 85vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0 20px;
    }
    .gemini-heading {
        font-size: 48px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 40px;
        background: linear-gradient(135deg, #FFFFFF 30%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Suggestion Cards */
    .suggestion-grid {
        display: flex;
        gap: 16px;
        margin-top: 30px;
        justify-content: center;
        flex-wrap: wrap;
        max-width: 800px;
    }
    .suggestion-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 20px;
        font-size: 14px;
        color: #CBD5E1;
        cursor: pointer;
        transition: all 0.2s ease;
        backdrop-filter: blur(12px);
    }
    .suggestion-card:hover {
        background: rgba(124, 58, 237, 0.15);
        border-color: rgba(124, 58, 237, 0.4);
        transform: translateY(-3px);
    }

    /* Glassmorphism General Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        color: #F8FAFC !important;
    }

    .footer {
        background: #0B1020;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 40px;
        text-align: center;
        color: #94A3B8;
        font-size: 14px;
    }
</style>

<div class="gemini-nav">
    <div class="gemini-logo">✨ AgentFlow AI</div>
    <div class="gemini-nav-links">
        <span>Pricing</span>
        <span>Contact</span>
        <span>Login</span>
    </div>
</div>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Collect 6 details: Name, Business Name, Service Required, Budget, Phone Number, Email Address. When collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_to_csv(filename, data_dict):
    df = pd.DataFrame([data_dict])
    if not os.path.exists(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

def generate_invoice_pdf(email, plan, amount):
    return f"AGENTFLOW AI - OFFICIAL INVOICE\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nCustomer: {email}\nPlan: {plan}\nAmount: {amount}\nStatus: SUCCESSFUL"

# Sidebar navigation to access separate pages (Admin, Pricing, Login, Booking)
st.sidebar.markdown("### ⚡ Navigation Hub")
page_choice = st.sidebar.radio("Go to Page", ["Gemini AI Homepage", "Pricing & Plans", "Contact & Booking", "Customer Portal", "Admin CRM Dashboard"])

if page_choice == "Gemini AI Homepage":
    if not st.session_state.chat_started:
        # Full-Screen Google Gemini Style Landing Screen
        st.markdown("""
            <div class="gemini-hero">
                <div class="gemini-heading">What can AgentFlow AI help you build today?</div>
            </div>
        """, unsafe_allow_html=True)

        # Centered Prompt Input Box
        col_c1, col_c_input, col_c3 = st.columns([1, 2, 1])
        with col_c_input:
            user_prompt = st.chat_input("Ask AgentFlow AI anything...")
            if user_prompt:
                st.session_state.chat_started = True
                st.session_state.messages.append({"role": "user", "content": user_prompt})
                st.rerun()

        # Suggestion Cards
        st.markdown("""
            <div style="display: flex; justify-content: center; margin-top: -120px;">
                <div class="suggestion-grid">
                    <div class="suggestion-card">• Build an AI Chatbot</div>
                    <div class="suggestion-card">• Create a Website</div>
                    <div class="suggestion-card">• Automate WhatsApp</div>
                    <div class="suggestion-card">• Build a CRM</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Active Chat View (Starts only after first message)
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #FFFFFF; margin-bottom: 30px;'>AgentFlow AI Workspace</h2>", unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]): st.markdown(msg["content"])
                
        if prompt := st.chat_input("Type your message..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            try:
                res = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.1-8b-instant", temperature=0.5).choices[0].message.content
                if "COMPLETE:" in res:
                    d = res.split("COMPLETE:")[1].strip().split("|")
                    if len(d) == 6:
                        save_to_csv("leads.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": d[0].strip(), "Business": d[1].strip(), "Service": d[2].strip(), "Budget": d[3].strip(), "Phone": d[4].strip(), "Email": d[5].strip(), "Status": "New", "Notes": "None"})
                    res = "Thank you! Our team will contact you soon."
                st.session_state.messages.append({"role": "assistant", "content": res})
                with st.chat_message("assistant"): st.markdown(res)
            except Exception as e: st.error(f"Error: {e}")

elif page_choice == "Pricing & Plans":
    st.markdown("<h2 style='text-align: center; font-weight: 800; margin-top: 40px; color: #FFFFFF;'>Transparent Pricing Plans</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Instant Razorpay secure checkout.</p>", unsafe_allow_html=True)
    
    if not st.session_state.checkout_active:
        pr1, pr2, pr3 = st.columns(3)
        with pr1:
            st.markdown('<div class="glass-card"><h3>Starter</h3><h2 style="color: #FFFFFF; margin: 20px 0;">₹999</h2><p style="color: #94A3B8;">Ideal for solo creators.</p></div>', unsafe_allow_html=True)
            if st.button("Select Starter", use_container_width=True): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with pr2:
            st.markdown('<div class="glass-card" style="border-color: rgba(124, 58, 237, 0.5);"><h3>Business</h3><h2 style="color: #FFFFFF; margin: 20px 0;">₹4,999</h2><p style="color: #94A3B8;">For growing companies.</p></div>', unsafe_allow_html=True)
            if st.button("Select Business", use_container_width=True): st.session_state.selected_plan = {"name": "Business", "price": "₹4,999"}; st.session_state.checkout_active = True; st.rerun()
        with pr3:
            st.markdown('<div class="glass-card"><h3>Enterprise</h3><h2 style="color: #FFFFFF; margin: 20px 0;">Custom</h2><p style="color: #94A3B8;">Tailored solutions.</p></div>', unsafe_allow_html=True)
            if st.button("Contact Sales", use_container_width=True): st.info("Use Contact page.")
    else:
        p = st.session_state.selected_plan
        col_chk1, col_chk2 = st.columns([1, 1])
        with col_chk1:
            st.markdown(f'<div class="glass-card"><h3>Razorpay Secure Checkout</h3><p style="color: #94A3B8; margin: 15px 0;">Plan: <b>{p["name"]}</b> | Amount: <b>{p["price"]}</b></p>', unsafe_allow_html=True)
            pay_method = st.selectbox("Payment Method", ["UPI", "Cards", "Net Banking", "Wallets"])
            email = st.text_input("Billing Email Address")
            if st.button("Pay Now via Razorpay", use_container_width=True):
                if email:
                    save_to_csv("paid_customers.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": p['name'], "Amount": p['price'], "Project Status": "In Progress", "Notes": f"Paid via {pay_method}"})
                    st.session_state.checkout_active = False
                    st.success("Payment Successful via Razorpay! Invoice generated.")
                    st.balloons()
                else: st.warning("Enter email.")
            if st.button("Back", use_container_width=True): st.session_state.checkout_active = False; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif page_choice == "Contact & Booking":
    st.markdown("<h2 style='text-align: center; font-weight: 800; margin-top: 40px; color: #FFFFFF;'>Contact & Book Meeting</h2>", unsafe_allow_html=True)
    con1, con2 = st.columns(2, gap="large")
    with con1:
        st.markdown("""
            <div class="glass-card">
                <h3>Get in Touch</h3>
                <p style="color: #94A3B8; margin: 15px 0 25px 0;">Reach out through our official channels:</p>
                <p>💬 <b>WhatsApp:</b> +91 98765 43210</p>
                <p>📧 <b>Email:</b> support@agentflow.ai</p>
            </div>
        """, unsafe_allow_html=True)
    with con2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Book Meeting Form")
        bname = st.text_input("Full Name", key="bk_name")
        bemail = st.text_input("Email Address", key="bk_email")
        bphone = st.text_input("Phone Number", key="bk_phone")
        bdate = st.date_input("Meeting Date", key="bk_date")
        bslot = st.selectbox("Time Slot", ["10:00 AM - 11:00 AM", "02:00 PM - 03:00 PM"])
        if st.button("Confirm Meeting", use_container_width=True):
            if bname and bemail:
                save_to_csv("bookings.csv", {"Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer Name": bname, "Email": bemail, "Phone": bphone, "Service": "Consultation", "Meeting Date": str(bdate), "Time Slot": bslot, "Status": "Pending", "Notes": "Booked"})
                st.success("Meeting booked successfully!")
            else: st.warning("Fill required details.")
        st.markdown('</div>', unsafe_allow_html=True)

elif page_choice == "Customer Portal":
    st.markdown("<h2 style='text-align: center; font-weight: 800; margin-top: 40px; color: #FFFFFF;'>Customer Portal</h2>", unsafe_allow_html=True)
    u = st.text_input("Username or Email")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u and p: st.success("Logged in successfully!")
        else: st.warning("Fill fields.")

elif page_choice == "Admin CRM Dashboard":
    st.markdown("<h2 style='text-align: center; font-weight: 800; margin-top: 40px; color: #FFFFFF;'>Admin CRM Dashboard</h2>", unsafe_allow_html=True)
    ap = st.text_input("Admin Password", type="password")
    if ap == "admin123":
        tot_l = len(pd.read_csv("leads.csv")) if os.path.exists("leads.csv") else 0
        tot_c = len(pd.read_csv("paid_customers.csv")) if os.path.exists("paid_customers.csv") else 0
        c1, c2 = st.columns(2)
        with c1: st.metric("Total Leads", tot_l)
        with c2: st.metric("Total Customers", tot_c)
        if os.path.exists("leads.csv"): st.dataframe(pd.read_csv("leads.csv"), use_container_width=True)
    elif ap:
        st.error("Incorrect password! Try 'admin123'")

st.markdown("""
    <div class="footer">
        <p>© 2026 AgentFlow AI. All rights reserved. | Privacy Policy | Terms | Refund Policy</p>
    </div>
""", unsafe_allow_html=True)
