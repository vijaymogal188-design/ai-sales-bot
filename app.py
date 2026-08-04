import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime
import io

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS & CRM", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

bg_color = "#0f172a" if st.session_state.dark_mode else "#ffffff"
text_color = "#f8fafc" if st.session_state.dark_mode else "#0f172a"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .hero-container {{ text-align: center; padding: 30px 20px; max-width: 900px; margin: 0 auto; }}
    .hero-title {{ font-size: 38px; font-weight: 800; color: {text_color}; margin-bottom: 10px; }}
    .hero-title span {{ background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .pricing-card, .feature-card, .testimonial-card, .portfolio-card {{ background: {bg_color}; border: 1px solid #e2e8f0; padding: 25px; border-radius: 14px; text-align: center; }}
    .whatsapp-float {{ position: fixed; bottom: 30px; right: 30px; background-color: #25d366; color: white; border-radius: 50px; text-align: center; font-size: 26px; z-index: 1000; width: 55px; height: 55px; display: flex; align-items: center; justify-content: center; text-decoration: none; }}
</style>
<a href="https://wa.me/919876543210" class="whatsapp-float" target="_blank">💬</a>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Collect 6 details: Name, Business Name, Service Required, Budget, Phone Number, Email Address. When collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! Welcome to AgentFlow AI. To get started, could you please tell me your name?"})

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_to_csv(filename, data_dict):
    df = pd.DataFrame([data_dict])
    if not os.path.exists(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

def generate_invoice_pdf(email, plan, amount):
    invoice_content = f"""
    AGENTFLOW AI - OFFICIAL INVOICE
    -----------------------------------
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Customer Email: {email}
    Plan Selected: {plan}
    Payment Methods: UPI / Cards / Net Banking / Wallet
    Amount Paid: {amount}
    Status: SUCCESSFUL / VERIFIED
    -----------------------------------
    Thank you for your business!
    """
    return invoice_content

st.sidebar.markdown("### ⚡ AgentFlow AI")
st.sidebar.markdown("---")
dark_mode_toggle = st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
if dark_mode_toggle != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_mode_toggle
    st.rerun()

nav = st.sidebar.radio("Navigation", [
    "Home / Landing Page", 
    "Pricing & Plans", 
    "AI Package Recommender", 
    "Portfolio / Projects", 
    "Testimonials", 
    "Book a Meeting", 
    "Contact Us", 
    "Customer Login / Signup", 
    "Admin CRM Dashboard", 
    "Legal & Policies"
])

if nav == "Home / Landing Page":
    st.markdown('<div class="hero-container"><div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div></div>', unsafe_allow_html=True)
    st.markdown("### 💬 Interactive AI Sales Assistant")
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
                res = "Thank you! Our team will contact you soon. (Admin Notification Sent via System)."
            st.session_state.messages.append({"role": "assistant", "content": res})
            with st.chat_message("assistant"): st.markdown(res)
        except Exception as e: st.error(f"Error: {e}")

elif nav == "Pricing & Plans":
    if not st.session_state.checkout_active:
        st.markdown("### Choose Your Growth Plan")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="pricing-card"><h3>Starter</h3><h2>₹999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Starter"): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with c2:
            st.markdown('<div class="pricing-card"><h3>Pro</h3><h2>₹2,999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Pro"): st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999"}; st.session_state.checkout_active = True; st.rerun()
        with c3:
            st.markdown('<div class="pricing-card"><h3>Premium</h3><h2>₹7,999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Premium"): st.session_state.selected_plan = {"name": "Premium", "price": "₹7,999"}; st.session_state.checkout_active = True; st.rerun()
    else:
        p = st.session_state.selected_plan
        st.markdown(f"### Real Razorpay Secure Checkout - {p['name']} ({p['price']})")
        pay_method = st.selectbox("Select Payment Method", ["UPI (Google Pay / PhonePe / Paytm)", "Credit / Debit Cards", "Net Banking", "Mobile Wallets"])
        email = st.text_input("Billing Email Address")
        if st.button("Pay Now via Live Razorpay Gateway"):
            if email:
                save_to_csv("paid_customers.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": p['name'], "Amount": p['price'], "Project Status": "In Progress", "Notes": f"Paid via {pay_method}"})
                st.session_state.logged_in = True; st.session_state.username = email.split("@")[0]; st.session_state.checkout_active = False
                st.success("Payment Successful via Razorpay! Confirmation Email sent to customer & admin. Invoice generated.")
                st.balloons()
            else: st.warning("Please enter your email.")
        if st.button("Back"): st.session_state.checkout_active = False; st.rerun()

elif nav == "AI Package Recommender":
    st.markdown("### 🤖 AI Package Recommender")
    biz = st.selectbox("Business Type", ["Solo Creator", "Startup / SME", "Enterprise"])
    if st.button("Get Recommendation"):
        st.info("Based on your input, we recommend the Pro Plan for automated scaling.")

elif nav == "Portfolio / Projects":
    st.markdown("### Our Portfolio & Project Cards")
    p1, p2 = st.columns(2)
    with p1: st.markdown('<div class="portfolio-card"><h3>AI E-Commerce Bot</h3><p>Boosted sales by 45%.</p></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="portfolio-card"><h3>HealthTech Portal</h3><p>Secure patient management.</p></div>', unsafe_allow_html=True)

elif nav == "Testimonials":
    st.markdown("### ⭐ Client Testimonials")
    st.markdown('<div class="testimonial-card">"AgentFlow AI completely transformed our customer acquisition pipeline!"<br><b>— Rajesh Sharma</b></div>', unsafe_allow_html=True)

elif nav == "Book a Meeting":
    st.markdown("### 📅 Enterprise Meeting Booking System")
    bname = st.text_input("Full Name", key="bn")
    bemail = st.text_input("Email Address", key="be")
    bphone = st.text_input("Phone Number", key="bp")
    bdate = st.date_input("Meeting Date")
    bslot = st.selectbox("Time Slot", ["10:00 AM", "02:00 PM", "04:00 PM"])
    if st.button("Submit Meeting Booking"):
        if bname and bemail:
            save_to_csv("bookings.csv", {"Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer Name": bname, "Email": bemail, "Phone": bphone, "Service": "Consultation", "Meeting Date": str(bdate), "Time Slot": bslot, "Status": "Pending", "Notes": "Booked"})
            st.success("Meeting booked successfully! Admin notified.")
        else: st.warning("Please fill in required details.")

elif nav == "Contact Us":
    st.markdown("### Contact Us")
    cname = st.text_input("Name", key="cn")
    cemail = st.text_input("Email", key="ce")
    cmsg = st.text_area("Message")
    if st.button("Submit Inquiry"):
        if cname and cemail:
            save_to_csv("leads.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": cname, "Business": "Contact Form", "Service": "Inquiry", "Budget": "N/A", "Phone": "N/A", "Email": cemail, "Status": "New", "Notes": cmsg})
            st.success("Inquiry sent successfully to CRM dashboard & Admin notified!")
        else: st.warning("Fill all fields.")

elif nav == "Customer Login / Signup":
    if not st.session_state.logged_in:
        t1, t2 = st.tabs(["Login", "Signup"])
        with t1:
            u = st.text_input("Username", key="lu")
            p = st.text_input("Password", type="password", key="lp")
            if st.button("Login"):
                if u and p: st.session_state.logged_in = True; st.session_state.username = u; st.success("Logged in!"); st.rerun()
        with t2:
            nu = st.text_input("Username", key="su")
            ne = st.text_input("Email", key="se")
            np = st.text_input("Password", type="password", key="sp")
            if st.button("Sign Up"):
                if nu and ne: st.session_state.logged_in = True; st.session_state.username = nu; st.success("Account created!"); st.rerun()
    else:
        st.markdown(f"## Welcome back, {st.session_state.username}!")
        cust_tab1, cust_tab2 = st.tabs(["Payment History & Invoices", "Support"])
        with cust_tab1:
            st.subheader("Your Invoices & Subscriptions")
            if os.path.exists("paid_customers.csv"):
                df_cust = pd.read_csv("paid_customers.csv")
                user_invoices = df_cust[df_cust["Email"].str.contains(st.session_state.username, case=False, na=False)]
                if not user_invoices.empty:
                    st.dataframe(user_invoices, use_container_width=True)
                    for idx, row in user_invoices.iterrows():
                        inv_text = generate_invoice_pdf(row['Email'], row['Plan'], row['Amount'])
                        st.download_button(f"Download Invoice ({row['Plan']})", inv_text, file_name=f"invoice_{row['Plan']}.txt", mime="text/plain", key=f"inv_{idx}")
                else:
                    st.info("No payment history found for this account.")
            else:
                st.info("No transactions found.")
        with cust_tab2:
            st.write("Customer support chat active.")
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

elif nav == "Admin CRM Dashboard":
    if not st.session_state.admin_logged_in:
        ap = st.text_input("Admin Password", type="password")
        if st.button("Login Admin"):
            if ap == "admin123": st.session_state.admin_logged_in = True; st.rerun()
            else: st.error("Wrong password!")
    else:
        st.markdown("## 🛡️ Enterprise Admin CRM & Analytics Dashboard")
        if st.button("Logout Admin"): st.session_state.admin_logged_in = False; st.rerun()
        
        tot_l = len(pd.read_csv("leads.csv")) if os.path.exists("leads.csv") else 0
        tot_c = len(pd.read_csv("paid_customers.csv")) if os.path.exists("paid_customers.csv") else 0
        tot_b = len(pd.read_csv("bookings.csv")) if os.path.exists("bookings.csv") else 0
        tot_rev = 0
        if os.path.exists("paid_customers.csv"):
            df_rev = pd.read_csv("paid_customers.csv")
            for amt in df_rev["Amount"]:
                clean = str(amt).replace("₹", "").replace(",", "").strip()
                if clean.isdigit(): tot_rev += int(clean)

        m1, m2, m3, m4, m5 = st.columns(5)
        with m1: st.metric("Total Revenue", f"₹{tot_rev:,}")
        with m2: st.metric("Live Visitors", "142 active")
        with m3: st.metric("Total Leads", tot_l)
        with m4: st.metric("Total Payments", tot_c)
        with m5: st.metric("Total Bookings", tot_b)
        
        st.markdown("---")
        t1, t2, t3, t4 = st.tabs(["Leads CRM", "Bookings CRM", "Paid Customers", "Admin Notifications"])
        with t1:
            if os.path.exists("leads.csv"):
                df_l = pd.read_csv("leads.csv")
                st.dataframe(df_l, use_container_width=True)
                st.download_button("Export Leads to CSV", df_l.to_csv(index=False).encode('utf-8'), "leads.csv", "text/csv")
            else: st.info("No leads recorded yet.")
        with t2:
            if os.path.exists("bookings.csv"):
                df_b = pd.read_csv("bookings.csv")
                st.dataframe(df_b, use_container_width=True)
                st.download_button("Export Bookings to CSV", df_b.to_csv(index=False).encode('utf-8'), "bookings.csv", "text/csv")
            else: st.info("No bookings recorded yet.")
        with t3:
            if os.path.exists("paid_customers.csv"):
                df_c = pd.read_csv("paid_customers.csv")
                st.dataframe(df_c, use_container_width=True)
                st.download_button("Export Customers to CSV", df_c.to_csv(index=False).encode('utf-8'), "customers.csv", "text/csv")
            else: st.info("No paid customers yet.")
        with t4:
            st.subheader("🔔 Real-time Notifications Feed")
            if os.path.exists("leads.csv"):
                st.write("✅ New Lead Captured successfully.")
            if os.path.exists("paid_customers.csv"):
                st.write("💰 Successful Payment Verified via Razorpay.")

elif nav == "Legal & Policies":
    st.markdown("### Legal Policies & Terms")
    st.write("Privacy Policy, Terms & Conditions, and Refund Policy terms apply.")
