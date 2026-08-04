import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS Platform", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit Default Sidebar / Navigation UI on Landing Page for Full Screen OpenAI/Stripe Style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Poppins', sans-serif;
        background-color: #0B1020;
        color: #F8FAFC;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #0B1020 60%);
        background-attachment: fixed;
    }

    /* Hide standard sidebar if needed, keep navigation functional */
    [data-testid="stSidebar"] {
        background-color: #0B1020;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(124, 58, 237, 0.4);
        box-shadow: 0 30px 60px rgba(124, 58, 237, 0.15);
    }

    /* Hero Section */
    .hero-container {
        padding: 40px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid rgba(124, 58, 237, 0.3);
        color: #a78bfa;
        font-weight: 600;
        font-size: 13px;
        padding: 8px 18px;
        border-radius: 50px;
        margin-bottom: 24px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .hero-title {
        font-size: 54px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
        margin-bottom: 20px;
        letter-spacing: -0.02em;
    }
    .hero-title span {
        background: linear-gradient(135deg, #a78bfa 0%, #6366f1 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #94a3b8;
        line-height: 1.6;
        margin-bottom: 35px;
    }

    /* Floating Chatbot Widget (Bottom Right) */
    .chatbot-float-container {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 380px;
        max-height: 500px;
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 20px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6);
        z-index: 9999;
        padding: 16px;
        display: flex;
        flex-direction: column;
    }

    /* Floating WhatsApp Button */
    .whatsapp-float {
        position: fixed;
        bottom: 25px;
        left: 25px;
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white;
        border-radius: 50px;
        text-align: center;
        font-size: 26px;
        box-shadow: 0 10px 25px rgba(37, 211, 102, 0.4);
        z-index: 1000;
        width: 55px;
        height: 55px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        transition: transform 0.3s ease;
    }
    .whatsapp-float:hover { transform: scale(1.1); }

    .footer {
        background: rgba(11, 16, 32, 0.8);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 60px 30px 30px 30px;
        margin-top: 80px;
    }
</style>

<a href="https://wa.me/919876543210" class="whatsapp-float" target="_blank" title="Chat on WhatsApp">💬</a>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Collect 6 details: Name, Business Name, Service Required, Budget, Phone Number, Email Address. When collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! Welcome to AgentFlow AI. What is your name?"})

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False
if "chat_open" not in st.session_state: st.session_state.chat_open = True

def save_to_csv(filename, data_dict):
    df = pd.DataFrame([data_dict])
    if not os.path.exists(filename): df.to_csv(filename, index=False)
    else: df.to_csv(filename, mode='a', header=False, index=False)

def generate_invoice_pdf(email, plan, amount):
    return f"""
    AGENTFLOW AI - OFFICIAL INVOICE
    -----------------------------------
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Customer Email: {email}
    Plan Selected: {plan}
    Amount Paid: {amount}
    Status: SUCCESSFUL / VERIFIED
    -----------------------------------
    Thank you for your business!
    """

st.sidebar.markdown("### ⚡ AgentFlow AI")
st.sidebar.caption("Enterprise SaaS & Automation")
st.sidebar.markdown("---")

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
    # OpenAI / Stripe / Vercel style Full-Screen Hero Section with 3D AI Illustration on right
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">✨ Next-Gen Enterprise AI & Automation</div>
        </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2 = st.columns([1.3, 1], gap="large")
    with col_h1:
        st.markdown("""
            <div class="hero-title">Scale Your Business with <span>AgentFlow AI</span></div>
            <div class="hero-subtitle">AI Chatbots, Websites, Mobile Apps & Business Automation for Modern Companies.</div>
        """, unsafe_allow_html=True)
        
        ch1, ch2 = st.columns(2)
        with ch1:
            if st.button("🚀 Get Free Demo", use_container_width=True):
                st.balloons()
        with ch2:
            if st.button("📅 Book a Meeting", use_container_width=True):
                st.info("Navigate to 'Book a Meeting' via sidebar.")

    with col_h2:
        # 3D AI Illustration Mockup Card
        st.markdown("""
            <div class="glass-card" style="padding: 40px; background: linear-gradient(135deg, rgba(124,58,237,0.2) 0%, rgba(59,130,246,0.1) 100%);">
                <h2 style="font-size: 48px; margin-bottom: 10px;">🤖⚡</h2>
                <h3 style="color: #a78bfa; margin-bottom: 10px;">Autonomous AI Core</h3>
                <p style="font-size: 14px; color: #94a3b8;">Real-time workflow pipelines, 24/7 conversational sales bots, and enterprise security.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Statistics Section
    st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 30px;'>Trusted by Industry Leaders Worldwide</h2>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1: st.markdown('<div class="glass-card"><h2 style="color: #a78bfa;">100+</h2><p style="color: #94a3b8;">Clients</p></div>', unsafe_allow_html=True)
    with s2: st.markdown('<div class="glass-card"><h2 style="color: #a78bfa;">500+</h2><p style="color: #94a3b8;">Projects</p></div>', unsafe_allow_html=True)
    with s3: st.markdown('<div class="glass-card"><h2 style="color: #a78bfa;">99%</h2><p style="color: #94a3b8;">Satisfaction</p></div>', unsafe_allow_html=True)
    with s4: st.markdown('<div class="glass-card"><h2 style="color: #a78bfa;">24/7</h2><p style="color: #94a3b8;">Support</p></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Floating Chatbot in Bottom-Right Corner
    st.markdown("""
        <div style="position: fixed; bottom: 25px; right: 25px; z-index: 9999;">
    """, unsafe_allow_html=True)
    
    with st.popover("💬 AI Chat Assistant"):
        st.write("### AI Sales Agent")
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

    st.markdown("</div>", unsafe_allow_html=True)

elif nav == "Pricing & Plans":
    if not st.session_state.checkout_active:
        st.markdown("### Choose Your Growth Plan")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="glass-card"><h3>Starter</h3><h2>₹999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Starter"): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with c2:
            st.markdown('<div class="glass-card"><h3>Pro</h3><h2>₹2,999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Pro"): st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999"}; st.session_state.checkout_active = True; st.rerun()
        with c3:
            st.markdown('<div class="glass-card"><h3>Premium</h3><h2>₹7,999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Premium"): st.session_state.selected_plan = {"name": "Premium", "price": "₹7,999"}; st.session_state.checkout_active = True; st.rerun()
    else:
        p = st.session_state.selected_plan
        st.markdown(f"### Razorpay Secure Checkout - {p['name']} ({p['price']})")
        pay_method = st.selectbox("Payment Method", ["UPI", "Cards", "Net Banking", "Wallets"])
        email = st.text_input("Billing Email")
        if st.button("Pay Now"):
            if email:
                save_to_csv("paid_customers.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": p['name'], "Amount": p['price'], "Project Status": "In Progress", "Notes": f"Paid via {pay_method}"})
                st.session_state.logged_in = True; st.session_state.username = email.split("@")[0]; st.session_state.checkout_active = False
                st.success("Payment Successful! Invoice generated.")
                st.balloons()
            else: st.warning("Enter email.")
        if st.button("Back"): st.session_state.checkout_active = False; st.rerun()

elif nav == "AI Package Recommender":
    st.markdown("### 🤖 AI Package Recommender")
    biz = st.selectbox("Business Type", ["Solo Creator", "Startup / SME", "Enterprise"])
    if st.button("Get Recommendation"):
        st.info("Based on your input, we recommend the Pro Plan.")

elif nav == "Portfolio / Projects":
    st.markdown("### Portfolio & Projects")
    p1, p2 = st.columns(2)
    with p1: st.markdown('<div class="glass-card"><h3>AI E-Commerce Bot</h3><p>Boosted sales by 45%.</p></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="glass-card"><h3>HealthTech Portal</h3><p>Secure patient portal.</p></div>', unsafe_allow_html=True)

elif nav == "Testimonials":
    st.markdown("### ⭐ Client Testimonials")
    st.markdown('<div class="glass-card">"AgentFlow AI transformed our lead pipeline!"<br><b>— Rajesh Sharma</b></div>', unsafe_allow_html=True)

elif nav == "Book a Meeting":
    st.markdown("### 📅 Book a Meeting")
    bname = st.text_input("Full Name", key="bn")
    bemail = st.text_input("Email", key="be")
    bphone = st.text_input("Phone", key="bp")
    bdate = st.date_input("Date")
    bslot = st.selectbox("Time Slot", ["10:00 AM", "02:00 PM", "04:00 PM"])
    if st.button("Submit Booking"):
        if bname and bemail:
            save_to_csv("bookings.csv", {"Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer Name": bname, "Email": bemail, "Phone": bphone, "Service": "Consultation", "Meeting Date": str(bdate), "Time Slot": bslot, "Status": "Pending", "Notes": "Booked"})
            st.success("Meeting booked successfully!")
        else: st.warning("Fill required details.")

elif nav == "Contact Us":
    st.markdown("### Contact Us")
    cname = st.text_input("Name", key="cn")
    cemail = st.text_input("Email", key="ce")
    cmsg = st.text_area("Message")
    if st.button("Submit Inquiry"):
        if cname and cemail:
            save_to_csv("leads.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": cname, "Business": "Contact Form", "Service": "Inquiry", "Budget": "N/A", "Phone": "N/A", "Email": cemail, "Status": "New", "Notes": cmsg})
            st.success("Inquiry sent successfully!")
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
        if os.path.exists("paid_customers.csv"):
            df_cust = pd.read_csv("paid_customers.csv")
            user_invoices = df_cust[df_cust["Email"].str.contains(st.session_state.username, case=False, na=False)]
            if not user_invoices.empty:
                st.dataframe(user_invoices, use_container_width=True)
                for idx, row in user_invoices.iterrows():
                    inv_text = generate_invoice_pdf(row['Email'], row['Plan'], row['Amount'])
                    st.download_button(f"Download Invoice ({row['Plan']})", inv_text, file_name=f"invoice_{row['Plan']}.txt", mime="text/plain", key=f"inv_{idx}")
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

elif nav == "Admin CRM Dashboard":
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
        tot_b = len(pd.read_csv("bookings.csv")) if os.path.exists("bookings.csv") else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Total Leads", tot_l)
        with c2: st.metric("Total Customers", tot_c)
        with c3: st.metric("Total Bookings", tot_b)
        
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

elif nav == "Legal & Policies":
    st.markdown("### Legal Policies & Terms")
    st.write("Privacy Policy, Terms & Conditions, and Refund Policy apply.")

st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px; max-width: 1200px; margin: 0 auto;">
            <div>
                <h3>⚡ AgentFlow AI</h3>
                <p style="color: #94a3b8; font-size: 14px; max-width: 300px;">Enterprise-grade AI automation and software development solutions.</p>
            </div>
            <div>
                <h4>Contact Desk</h4>
                <p style="color: #94a3b8; font-size: 14px;">📧 Email: support@agentflow.ai</p>
                <p style="color: #94a3b8; font-size: 14px;">💬 WhatsApp: +91 98765 43210</p>
            </div>
        </div>
        <div style="text-align: center; border-top: 1px solid rgba(255,255,255,0.08); margin-top: 40px; padding-top: 20px; color: #64748b; font-size: 14px;">
            <p>© 2026 AgentFlow AI. All rights reserved.</p>
        </div>
    </div>
""", unsafe_allow_html=True)
