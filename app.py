import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #0f172a; }
    .stApp { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    .hero-container { text-align: center; padding: 50px 20px 30px 20px; max-width: 900px; margin: 0 auto; }
    .hero-badge { display: inline-block; background: #ede9fe; color: #7c3aed; font-weight: 700; font-size: 13px; padding: 6px 16px; border-radius: 50px; margin-bottom: 16px; }
    .hero-title { font-size: 46px; font-weight: 800; color: #0f172a; line-height: 1.2; margin-bottom: 16px; }
    .hero-title span { background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .section-title { text-align: center; font-size: 28px; font-weight: 800; color: #0f172a; margin-top: 50px; margin-bottom: 10px; }
    .pricing-card, .feature-card, .testimonial-card, .portfolio-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 16px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    .footer { background: #0f172a; color: #f8fafc; padding: 50px 30px 20px 30px; border-top: 1px solid #1e293b; margin-top: 60px; border-radius: 16px 16px 0 0; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = "You are an expert AI Sales Agent for AgentFlow AI. Collect 6 details: Name, Business, Service, Budget, Phone, Email. When collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! Welcome to AgentFlow AI. What is your name?"})

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_user_to_csv(username, email, password):
    df = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Username": username, "Email": email, "Password": password}])
    if not os.path.exists("users.csv"): df.to_csv("users.csv", index=False)
    else: df.to_csv("users.csv", mode='a', header=False, index=False)

def save_lead_to_csv(data_list):
    df = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": data_list[0].strip(), "Business": data_list[1].strip(), "Service": data_list[2].strip(), "Budget": data_list[3].strip(), "Phone": data_list[4].strip(), "Email": data_list[5].strip(), "Status": "New", "Notes": "None"}])
    if not os.path.exists("leads.csv"): df.to_csv("leads.csv", index=False)
    else: df.to_csv("leads.csv", mode='a', header=False, index=False)

def save_paid_customer(email, plan_name, amount):
    df = pd.DataFrame([{"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": plan_name, "Amount": amount, "Project Status": "In Progress", "Notes": "Paid"}])
    if not os.path.exists("paid_customers.csv"): df.to_csv("paid_customers.csv", index=False)
    else: df.to_csv("paid_customers.csv", mode='a', header=False, index=False)

def save_booking_to_csv(name, email, phone, service, date, time_slot):
    df = pd.DataFrame([{"Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer Name": name, "Email": email, "Phone": phone, "Service": service, "Meeting Date": str(date), "Time Slot": str(time_slot), "Status": "Pending", "Notes": "Scheduled"}])
    if not os.path.exists("bookings.csv"): df.to_csv("bookings.csv", index=False)
    else: df.to_csv("bookings.csv", mode='a', header=False, index=False)

def generate_invoice_pdf(email, plan, amount):
    return f"INVOICE\nDate: {datetime.now()}\nEmail: {email}\nPlan: {plan}\nAmount: {amount}\nStatus: PAID"

st.sidebar.markdown("### ⚡ AgentFlow AI")
nav_choice = st.sidebar.radio("Navigation", [
    "Home / Landing Page", "Pricing & Plans", "AI Package Recommender",
    "Portfolio / Projects", "Testimonials", "Book a Meeting",
    "Contact Us", "Customer Login / Signup", "Admin CRM Dashboard", "Legal & Policies"
])

if nav_choice == "Home / Landing Page":
    st.markdown('<div class="hero-container"><div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div></div>', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]): st.markdown(message["content"])
    if prompt := st.chat_input("Type your message..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.1-8b-instant", temperature=0.5).choices[0].message.content
                if "COMPLETE:" in res:
                    ld = res.split("COMPLETE:")[1].strip().split("|")
                    if len(ld) == 6: save_lead_to_csv(ld)
                    res = "Thank you! Our team will contact you soon."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e: st.error(f"Error: {e}")

elif nav_choice == "Pricing & Plans":
    if not st.session_state.checkout_active:
        st.markdown('<div class="section-title">Choose Your Plan</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="pricing-card"><h3>Starter</h3><h2>₹999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Starter"): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with c2:
            st.markdown('<div class="pricing-card"><h3>Pro</h3><h2>₹2,999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Pro"): st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999"}; st.session_state.checkout_active = True; st.rerun()
        with c3:
            st.markdown('<div class="pricing-card"><h3>Enterprise</h3><h2>₹7,999</h2></div>', unsafe_allow_html=True)
            if st.button("Buy Enterprise"): st.session_state.selected_plan = {"name": "Enterprise", "price": "₹7,999"}; st.session_state.checkout_active = True; st.rerun()
    else:
        plan = st.session_state.selected_plan
        st.subheader(f"Checkout - {plan['name']}")
        email_in = st.text_input("Billing Email")
        if st.button("Pay via Razorpay"):
            if email_in:
                save_paid_customer(email_in, plan['name'], plan['price'])
                st.session_state.logged_in = True
                st.session_state.username = email_in.split("@")[0]
                st.session_state.user_email = email_in
                st.session_state.checkout_active = False
                st.success("Payment Successful!")
                st.rerun()
            else: st.warning("Enter email.")

elif nav_choice == "AI Package Recommender":
    st.subheader("AI Package Recommender")
    b_type = st.selectbox("Business Type", ["Solo Creator", "Startup", "Enterprise"])
    if st.button("Get Recommendation"):
        st.info("Recommended Plan: Pro Plan (₹2,999)")

elif nav_choice == "Portfolio / Projects":
    st.subheader("Portfolio")
    st.write("Explore our deployed projects.")

elif nav_choice == "Testimonials":
    st.subheader("Testimonials")
    st.write("Client reviews and success stories.")

elif nav_choice == "Book a Meeting":
    st.subheader("Book Meeting")
    bn = st.text_input("Name")
    be = st.text_input("Email")
    bp = st.text_input("Phone")
    bd = st.date_input("Date")
    if st.button("Book Now"):
        if bn and be:
            save_booking_to_csv(bn, be, bp, "Consultation", bd, "10:00 AM")
            st.success("Meeting Booked Successfully!")
        else: st.warning("Fill required fields.")

elif nav_choice == "Contact Us":
    st.subheader("Contact Us")
    cn = st.text_input("Name")
    ce = st.text_input("Email")
    cm = st.text_area("Message")
    if st.button("Send Inquiry"):
        if cn and ce:
            save_lead_to_csv([cn, "Contact Form", "General", "Custom", "N/A", ce])
            st.success("Inquiry Sent!")
        else: st.warning("Fill all fields.")

elif nav_choice == "Customer Login / Signup":
    if not st.session_state.logged_in:
        st.subheader("Customer Portal")
        lu = st.text_input("Login Username")
        lp = st.text_input("Login Password", type="password")
        if st.button("Login"):
            if lu and lp:
                st.session_state.logged_in = True
                st.session_state.username = lu
                st.session_state.user_email = f"{lu}@agentflow.ai"
                st.success("Login Successful!")
                st.rerun()
            else: st.warning("Fill fields.")

        st.markdown("---")
        su = st.text_input("Signup Username")
        se = st.text_input("Signup Email")
        sp = st.text_input("Signup Password", type="password")
        if st.button("Signup"):
            if su and se and sp:
                save_user_to_csv(su, se, sp)
                st.session_state.logged_in = True
                st.session_state.username = su
                st.session_state.user_email = se
                st.success("Account Created!")
                st.rerun()
            else: st.warning("Fill fields.")
    else:
        st.subheader(f"Welcome, {st.session_state.username}!")
        t1, t2 = st.tabs(["Dashboard", "Support"])
        with t1: st.metric("Project Status", "In Progress", "65%")
        with t2: st.write("Support Chat Active")
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

elif nav_choice == "Admin CRM Dashboard":
    if not st.session_state.admin_logged_in:
        ap = st.text_input("Admin Password", type="password")
        if st.button("Login Admin"):
            if ap == "admin123": st.session_state.admin_logged_in = True; st.rerun()
            else: st.error("Incorrect password")
    else:
        st.subheader("Admin CRM Dashboard")
        u_df = pd.read_csv("users.csv") if os.path.exists("users.csv") else pd.DataFrame()
        l_df = pd.read_csv("leads.csv") if os.path.exists("leads.csv") else pd.DataFrame()
        b_df = pd.read_csv("bookings.csv") if os.path.exists("bookings.csv") else pd.DataFrame()
        c_df = pd.read_csv("paid_customers.csv") if os.path.exists("paid_customers.csv") else pd.DataFrame()

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("Users", len(u_df))
        with m2: st.metric("Leads", len(l_df))
        with m3: st.metric("Bookings", len(b_df))
        with m4: st.metric("Customers", len(c_df))

        t1, t2, t3, t4 = st.tabs(["Users", "Leads", "Bookings", "Customers"])
        with t1: st.dataframe(u_df)
        with t2: st.dataframe(l_df)
        with t3: st.dataframe(b_df)
        with t4: st.dataframe(c_df)
        if st.button("Admin Logout"): st.session_state.admin_logged_in = False; st.rerun()

elif nav_choice == "Legal & Policies":
    st.subheader("Legal Policies")
    st.write("Privacy Policy, Terms of Service, and Refund Policy terms apply.")

st.markdown('<div class="footer"><p>© 2026 AgentFlow AI. All rights reserved.</p></div>', unsafe_allow_html=True)
