import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS", 
    page_icon="⚡", 
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #0f172a; }
    .hero-container { text-align: center; padding: 40px 20px; }
    .hero-title { font-size: 42px; font-weight: 800; color: #0f172a; }
    .pricing-card, .feature-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .footer { background: #0f172a; color: #f8fafc; padding: 40px; margin-top: 50px; border-radius: 12px 12px 0 0; text-align: center; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Collect 6 details: 
1. Name, 2. Business Name, 3. Service Required, 4. Budget, 5. Phone Number, 6. Email Address. 
When collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! Welcome to AgentFlow AI. What is your name?"})

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_csv(filename, data):
    df = pd.DataFrame([data])
    if not os.path.exists(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

st.sidebar.markdown("### ⚡ AgentFlow AI")
nav = st.sidebar.radio("Navigation", ["Home", "Pricing", "Book Meeting", "Login / Signup", "Admin CRM"])

if nav == "Home":
    st.markdown('<div class="hero-container"><div class="hero-title">Scale Your Growth with AgentFlow AI</div></div>', unsafe_allow_html=True)
    st.subheader("💬 AI Sales Assistant")
    for m in st.session_state.messages:
        if m["role"] != "system":
            with st.chat_message(m["role"]): st.markdown(m["content"])
    if prompt := st.chat_input("Type your message..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.1-8b-instant", temperature=0.5).choices[0].message.content
                if "COMPLETE:" in res:
                    ld = res.split("COMPLETE:")[1].strip().split("|")
                    if len(ld) == 6: save_csv("leads.csv", {"Date": datetime.now(), "Name": ld[0], "Business": ld[1], "Service": ld[2], "Budget": ld[3], "Phone": ld[4], "Email": ld[5]})
                    res = "Thank you! Our team will contact you soon."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e: st.error(f"Error: {e}")

elif nav == "Pricing":
    if not st.session_state.checkout_active:
        st.markdown("<h2 style='text-align:center;'>Pricing Plans</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="pricing-card"><h3>Starter</h3><h2>₹999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Starter"): st.session_state.plan = ("Starter", "₹999"); st.session_state.checkout_active = True; st.rerun()
        with c2:
            st.markdown('<div class="pricing-card"><h3>Pro</h3><h2>₹2,999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Pro"): st.session_state.plan = ("Pro", "₹2,999"); st.session_state.checkout_active = True; st.rerun()
        with c3:
            st.markdown('<div class="pricing-card"><h3>Enterprise</h3><h2>₹7,999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Enterprise"): st.session_state.plan = ("Enterprise", "₹7,999"); st.session_state.checkout_active = True; st.rerun()
    else:
        st.subheader("Secure Checkout")
        email = st.text_input("Billing Email")
        if st.button("Complete Payment"):
            if email:
                save_csv("paid_customers.csv", {"Date": datetime.now(), "Email": email, "Plan": st.session_state.plan[0], "Amount": st.session_state.plan[1]})
                st.session_state.logged_in = True
                st.session_state.username = email.split("@")[0]
                st.session_state.checkout_active = False
                st.success("Payment Successful!")
                st.rerun()
            else: st.warning("Enter email.")

elif nav == "Book Meeting":
    st.subheader("Book a Consultation")
    n = st.text_input("Name")
    e = st.text_input("Email")
    p = st.text_input("Phone")
    d = st.date_input("Date")
    if st.button("Book"):
        if n and e:
            save_csv("bookings.csv", {"Date": datetime.now(), "Name": n, "Email": e, "Phone": p, "MeetingDate": d})
            st.success("Meeting Booked Successfully!")
        else: st.warning("Fill required fields.")

elif nav == "Login / Signup":
    if not st.session_state.logged_in:
        st.subheader("Customer Portal")
        tab1, tab2 = st.tabs(["Login", "Signup"])
        with tab1:
            with st.form("l_form"):
                lu = st.text_input("Username")
                lp = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if lu and lp:
                        st.session_state.logged_in = True
                        st.session_state.username = lu
                        st.success("Login Successful!")
                        st.rerun()
        with tab2:
            with st.form("s_form"):
                su = st.text_input("New Username")
                se = st.text_input("Email")
                sp = st.text_input("New Password", type="password")
                if st.form_submit_button("Signup"):
                    if su and se and sp:
                        save_csv("users.csv", {"Date": datetime.now(), "Username": su, "Email": se, "Password": sp})
                        st.session_state.logged_in = True
                        st.session_state.username = su
                        st.success("Account Created Successfully!")
                        st.rerun()
    else:
        st.write(f"Welcome back, {st.session_state.username}!")
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

elif nav == "Admin CRM":
    if not st.session_state.admin_logged_in:
        ap = st.text_input("Admin Password", type="password")
        if st.button("Admin Login"):
            if ap == "admin123": st.session_state.admin_logged_in = True; st.rerun()
            else: st.error("Wrong password")
    else:
        st.subheader("Admin CRM Dashboard")
        t1, t2, t3, t4 = st.tabs(["Users", "Leads", "Bookings", "Customers"])
        with t1:
            if os.path.exists("users.csv"): st.dataframe(pd.read_csv("users.csv"))
            else: st.info("No users found.")
        with t2:
            if os.path.exists("leads.csv"): st.dataframe(pd.read_csv("leads.csv"))
            else: st.info("No leads found.")
        with t3:
            if os.path.exists("bookings.csv"): st.dataframe(pd.read_csv("bookings.csv"))
            else: st.info("No bookings found.")
        with t4:
            if os.path.exists("paid_customers.csv"): st.dataframe(pd.read_csv("paid_customers.csv"))
            else: st.info("No customers found.")
        if st.button("Admin Logout"): st.session_state.admin_logged_in = False; st.rerun()

st.markdown('<div class="footer"><p>© 2026 AgentFlow AI. All rights reserved.</p></div>', unsafe_allow_html=True)
