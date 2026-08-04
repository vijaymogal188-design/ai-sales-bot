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

def generate_invoice_pdf(email, plan, amount):
    return f"""
    AGENTFLOW AI - INVOICE
    -----------------------------------
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Email: {email}
    Plan: {plan}
    Amount: {amount}
    Status: PAID
    -----------------------------------
    """

st.sidebar.markdown("### ⚡ AgentFlow AI")
nav = st.sidebar.radio("Navigation", ["Home", "Pricing", "AI Recommender", "Portfolio", "Testimonials", "Book Meeting", "Contact Us", "Login / Signup", "Admin CRM", "Legal & Policies"])

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
                save_csv("paid_customers.csv", {"Date": datetime.now(), "Email": email, "Plan": st.session_state.plan[0], "Amount": st.session_state.plan[1], "Project Status": "In Progress"})
                st.session_state.logged_in = True
                st.session_state.username = email.split("@")[0]
                st.session_state.user_email = email
                st.session_state.checkout_active = False
                st.success("Payment Successful!")
                st.rerun()
            else: st.warning("Enter email.")

elif nav == "AI Recommender":
    st.subheader("AI Package Recommender")
    b_type = st.selectbox("Business Type", ["Solo Creator", "Startup", "Enterprise"])
    if st.button("Get Recommendation"):
        st.info("Recommended Plan based on your profile: Pro Plan (₹2,999)")

elif nav == "Portfolio":
    st.subheader("Our Portfolio")
    st.write("Explore our successfully deployed AI and automation projects.")

elif nav == "Testimonials":
    st.subheader("Client Testimonials")
    st.write("Hear what industry leaders say about our solutions.")

elif nav == "Book Meeting":
    st.subheader("Book a Consultation")
    n = st.text_input("Name")
    e = st.text_input("Email")
    p = st.text_input("Phone")
    d = st.date_input("Date")
    if st.button("Book Meeting"):
        if n and e:
            save_csv("bookings.csv", {"Date": datetime.now(), "Name": n, "Email": e, "Phone": p, "MeetingDate": d})
            st.success("Meeting Booked Successfully!")
        else: st.warning("Fill required fields.")

elif nav == "Contact Us":
    st.subheader("Contact Us")
    cn = st.text_input("Your Name")
    ce = st.text_input("Your Email")
    cm = st.text_area("Your Message")
    if st.button("Send Message"):
        if cn and ce and cm:
            save_csv("leads.csv", {"Date": datetime.now(), "Name": cn, "Business": "Contact Form", "Service": "Inquiry", "Budget": "N/A", "Phone": "N/A", "Email": ce})
            st.success("Message Sent Successfully!")

elif nav == "Login / Signup":
    if not st.session_state.logged_in:
        st.subheader("Customer Portal Authentication")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Login")
            lu = st.text_input("Username", key="l_u")
            lp = st.text_input("Password", type="password", key="l_p")
            if st.button("Login Now"):
                if lu and lp:
                    st.session_state.logged_in = True
                    st.session_state.username = lu
                    st.session_state.user_email = f"{lu}@agentflow.ai"
                    st.success("Login Successful!")
                    st.rerun()
                else: st.warning("Fill fields.")
        with col2:
            st.markdown("### Signup")
            su = st.text_input("Username", key="s_u")
            se = st.text_input("Email", key="s_e")
            sp = st.text_input("Password", type="password", key="s_p")
            if st.button("Create Account"):
                if su and se and sp:
                    save_csv("users.csv", {"Date": datetime.now(), "Username": su, "Email": se, "Password": sp})
                    st.session_state.logged_in = True
                    st.session_state.username = su
                    st.session_state.user_email = se
                    st.success("Account Created!")
                    st.rerun()
                else: st.warning("Fill fields.")
    else:
        st.subheader(f"Welcome, {st.session_state.username}!")
        t1, t2 = st.tabs(["Dashboard", "Invoices"])
        with t1:
            st.metric("Project Status", "In Progress", "65%")
        with t2:
            if os.path.exists("paid_customers.csv"):
                df = pd.read_csv("paid_customers.csv")
                st.dataframe(df)
            else: st.info("No invoices found.")
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
            else: st.info("No users.")
        with t2:
            if os.path.exists("leads.csv"): st.dataframe(pd.read_csv("leads.csv"))
            else: st.info("No leads.")
        with t3:
            if os.path.exists("bookings.csv"): st.dataframe(pd.read_csv("bookings.csv"))
            else: st.info("No bookings.")
        with t4:
            if os.path.exists("paid_customers.csv"): st.dataframe(pd.read_csv("paid_customers.csv"))
            else: st.info("No customers.")
        if st.button("Admin Logout"): st.session_state.admin_logged_in = False; st.rerun()

elif nav == "Legal & Policies":
    st.subheader("Legal Policies & Terms")
    st.write("Privacy Policy, Terms of Service, and Refund Policy apply.")

st.markdown('<div class="footer"><p>© 2026 AgentFlow AI. All rights reserved.</p></div>', unsafe_allow_html=True)
