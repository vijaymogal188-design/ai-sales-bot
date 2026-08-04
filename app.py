import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(page_title="AgentFlow AI | CRM", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .hero-container { text-align: center; padding: 30px 20px; max-width: 900px; margin: 0 auto; }
    .hero-title { font-size: 38px; font-weight: 800; color: #0f172a; margin-bottom: 10px; }
    .hero-title span { background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .pricing-card, .feature-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 14px; text-align: center; }
    .whatsapp-float { position: fixed; bottom: 30px; right: 30px; background-color: #25d366; color: white; border-radius: 50px; text-align: center; font-size: 26px; z-index: 1000; width: 55px; height: 55px; display: flex; align-items: center; justify-content: center; text-decoration: none; }
</style>
<a href="https://wa.me/919876543210" class="whatsapp-float" target="_blank">💬</a>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an AI Sales Agent. Collect 6 details: Name, Business, Service, Budget, Phone, Email. When collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! Welcome to AgentFlow AI. What is your name?"})

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_to_csv(filename, data_dict):
    df = pd.DataFrame([data_dict])
    if not os.path.exists(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

st.sidebar.markdown("### ⚡ AgentFlow AI")
nav = st.sidebar.radio("Navigation", ["Home", "Pricing", "Book Meeting", "Contact Us", "Login", "Admin CRM"])

if nav == "Home":
    st.markdown('<div class="hero-container"><div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div></div>', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if prompt := st.chat_input("Type message..."):
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

elif nav == "Pricing":
    if not st.session_state.checkout_active:
        st.markdown("### Choose Plan")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="pricing-card"><h3>Starter</h3><h2>₹999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Starter"): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with c2:
            st.markdown('<div class="pricing-card"><h3>Pro</h3><h2>₹2,999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Pro"): st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999"}; st.session_state.checkout_active = True; st.rerun()
        with c3:
            st.markdown('<div class="pricing-card"><h3>Premium</h3><h2>₹7,999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Premium"): st.session_state.selected_plan = {"name": "Premium", "price": "₹7,999"}; st.session_state.checkout_active = True; st.rerun()
    else:
        p = st.session_state.selected_plan
        st.markdown(f"### Checkout - {p['name']} ({p['price']})")
        email = st.text_input("Billing Email")
        if st.button("Pay Securely"):
            if email:
                save_to_csv("paid_customers.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": p['name'], "Amount": p['price'], "Project Status": "In Progress", "Notes": "Paid"})
                st.session_state.logged_in = True; st.session_state.username = email.split("@")[0]; st.session_state.checkout_active = False
                st.success("Payment successful! Redirecting...")
                st.balloons(); st.rerun()
            else: st.warning("Enter email.")
        if st.button("Back"): st.session_state.checkout_active = False; st.rerun()

elif nav == "Book Meeting":
    st.markdown("### Book a Strategy Consultation")
    name = st.text_input("Name", key="bn")
    email = st.text_input("Email", key="be")
    phone = st.text_input("Phone", key="bp")
    date = st.date_input("Date")
    slot = st.selectbox("Slot", ["10:00 AM", "02:00 PM", "04:00 PM"])
    if st.button("Confirm Booking"):
        if name and email:
            save_to_csv("bookings.csv", {"Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer Name": name, "Email": email, "Phone": phone, "Service": "Consultation", "Meeting Date": str(date), "Time Slot": slot, "Status": "Pending", "Notes": "Booked"})
            st.success("Meeting booked successfully!")
        else: st.warning("Fill required fields.")

elif nav == "Contact Us":
    st.markdown("### Contact Us")
    cname = st.text_input("Name", key="cn")
    cemail = st.text_input("Email", key="ce")
    cmsg = st.text_area("Message")
    if st.button("Submit"):
        if cname and cemail:
            save_to_csv("leads.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": cname, "Business": "Contact Form", "Service": "Inquiry", "Budget": "N/A", "Phone": "N/A", "Email": cemail, "Status": "New", "Notes": cmsg})
            st.success("Inquiry sent to CRM!")
        else: st.warning("Fill all fields.")

elif nav == "Login":
    if not st.session_state.logged_in:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if u and p: st.session_state.logged_in = True; st.session_state.username = u; st.success("Logged in!"); st.rerun()
    else:
        st.markdown(f"## Welcome, {st.session_state.username}!")
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

elif nav == "Admin CRM":
    if not st.session_state.admin_logged_in:
        ap = st.text_input("Admin Password", type="password")
        if st.button("Login Admin"):
            if ap == "admin123": st.session_state.admin_logged_in = True; st.rerun()
            else: st.error("Wrong password!")
    else:
        st.markdown("## 🛡️ Admin CRM Dashboard")
        if st.button("Logout Admin"): st.session_state.admin_logged_in = False; st.rerun()
        
        tot_l = len(pd.read_csv("leads.csv")) if os.path.exists("leads.csv") else 0
        tot_c = len(pd.read_csv("paid_customers.csv")) if os.path.exists("paid_customers.csv") else 0
        
        c1, c2 = st.columns(2)
        with c1: st.metric("Total Leads", tot_l)
        with c2: st.metric("Total Customers", tot_c)
        
        st.markdown("---")
        t1, t2, t3 = st.tabs(["Leads", "Bookings", "Customers"])
        with t1:
            if os.path.exists("leads.csv"): st.dataframe(pd.read_csv("leads.csv"), use_container_width=True)
            else: st.info("No leads yet.")
        with t2:
            if os.path.exists("bookings.csv"): st.dataframe(pd.read_csv("bookings.csv"), use_container_width=True)
            else: st.info("No bookings yet.")
        with t3:
            if os.path.exists("paid_customers.csv"): st.dataframe(pd.read_csv("paid_customers.csv"), use_container_width=True)
            else: st.info("No customers yet.")
