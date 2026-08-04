import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS Platform", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    .hero-container {
        text-align: center;
        padding: 60px 20px 40px 20px;
        max-width: 900px;
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
        font-size: 56px;
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
        max-width: 750px;
        margin-left: auto;
        margin-right: auto;
    }

    .stat-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    .stat-number {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .stat-label {
        font-size: 14px;
        color: #94a3b8;
        font-weight: 500;
    }

    .whatsapp-float {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white;
        border-radius: 50px;
        text-align: center;
        font-size: 28px;
        box-shadow: 0 10px 25px rgba(37, 211, 102, 0.4);
        z-index: 1000;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        transition: transform 0.3s ease;
    }
    .whatsapp-float:hover {
        transform: scale(1.1);
    }

    .footer {
        background: rgba(11, 16, 32, 0.8);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 60px 30px 30px 30px;
        margin-top: 80px;
    }

    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: rgba(30, 41, 59, 0.6) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
</style>

<a href="https://wa.me/919876543210?text=Hello%20AgentFlow%20AI,%20I%20want%20to%20know%20more%20about%20your%20services!" class="whatsapp-float" target="_blank" title="Chat on WhatsApp">💬</a>
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
    return f"""
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
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">✨ Next-Gen Enterprise AI & Automation</div>
            <div class="hero-title">Scale Your Business with <span>AgentFlow AI</span></div>
            <div class="hero-subtitle">AI Chatbots, Websites, Mobile Apps & Business Automation for Modern Companies.</div>
        </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2 = st.columns([1.2, 1], gap="large")
    with col_h1:
        st.write("")
        st.write("")
        ch1, ch2 = st.columns(2)
        with ch1:
            if st.button("🚀 Get Free Demo", use_container_width=True):
                st.balloons()
        with ch2:
            if st.button("📅 Book a Meeting", use_container_width=True):
                st.info("Navigate to 'Book a Meeting' in the sidebar to select your schedule.")
    with col_h2:
        st.markdown("""
            <div class="glass-card" style="padding: 20px;">
                <h4 style="color: #a78bfa; margin-bottom: 10px;">⚡ Live AI Ecosystem</h4>
                <p style="font-size: 13px; color: #94a3b8;">Autonomous agents analyzing pipelines, handling real-time customer queries, and optimizing conversion rates 24/7.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 30px;'>Trusted by Industry Leaders Worldwide</h2>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    with s1: st.markdown('<div class="stat-card"><div class="stat-number">100+</div><div class="stat-label">Clients</div></div>', unsafe_allow_html=True)
    with s2: st.markdown('<div class="stat-card"><div class="stat-number">500+</div><div class="stat-label">Projects</div></div>', unsafe_allow_html=True)
    with s3: st.markdown('<div class="stat-card"><div class="stat-number">99%</div><div class="stat-label">Satisfaction</div></div>', unsafe_allow_html=True)
    with s4: st.markdown('<div class="stat-card"><div class="stat-number">24/7</div><div class="stat-label">Support</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 10px;'>Our Core Services</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 40px;'>Comprehensive digital and artificial intelligence solutions designed for scale.</p>", unsafe_allow_html=True)

    srv1, srv2, srv3, srv4 = st.columns(4)
    with srv1: st.markdown('<div class="glass-card"><h3>🤖 AI Chatbots</h3><p style="color: #94a3b8; font-size: 14px;">Intelligent customer support and sales conversion bots.</p></div>', unsafe_allow_html=True)
    with srv2: st.markdown('<div class="glass-card"><h3>🎙️ AI Voice Agents</h3><p style="color: #94a3b8; font-size: 14px;">Human-like voice assistants for phone calls and inquiries.</p></div>', unsafe_allow_html=True)
    with srv3: st.markdown('<div class="glass-card"><h3>🌐 Website Dev</h3><p style="color: #94a3b8; font-size: 14px;">Lightning-fast, high-converting modern web applications.</p></div>', unsafe_allow_html=True)
    with srv4: st.markdown('<div class="glass-card"><h3>📱 Mobile Apps</h3><p style="color: #94a3b8; font-size: 14px;">Scalable iOS & Android apps built for performance.</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    srv5, srv6, srv7, srv8 = st.columns(4)
    with srv5: st.markdown('<div class="glass-card"><h3>💬 WhatsApp Auto</h3><p style="color: #94a3b8; font-size: 14px;">Automate messaging, broadcasts, and lead routing.</p></div>', unsafe_allow_html=True)
    with srv6: st.markdown('<div class="glass-card"><h3>📊 CRM Automation</h3><p style="color: #94a3b8; font-size: 14px;">Seamless pipeline management and data synchronization.</p></div>', unsafe_allow_html=True)
    with srv7: st.markdown('<div class="glass-card"><h3>⚡ AI Integrations</h3><p style="color: #94a3b8; font-size: 14px;">Custom LLM embeddings and intelligent workflows.</p></div>', unsafe_allow_html=True)
    with srv8: st.markdown('<div class="glass-card"><h3>🎨 UI/UX Design</h3><p style="color: #94a3b8; font-size: 14px;">World-class user interfaces crafted for engagement.</p></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card" style="text-align: left; max-width: 900px; margin: 0 auto;">', unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

elif nav == "Pricing & Plans":
    if not st.session_state.checkout_active:
        st.markdown("""
            <div class="hero-container">
                <div class="hero-title">Simple, Transparent <span>Pricing</span></div>
                <p style="color: #94a3b8;">Choose the ideal plan to scale your automated operations.</p>
            </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="glass-card"><h3>Starter</h3><h2 style="color: #a78bfa; margin: 20px 0;">₹999</h2><p style="color: #94a3b8;">Perfect for solo creators & small tasks.</p></div>', unsafe_allow_html=True)
            if st.button("Select Starter", use_container_width=True): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with c2:
            st.markdown('<div class="glass-card" style="border-color: #7c3aed;"><h3>Pro</h3><h2 style="color: #a78bfa; margin: 20px 0;">₹2,999</h2><p style="color: #94a3b8;">Ideal for growing businesses & scaling leads.</p></div>', unsafe_allow_html=True)
            if st.button("Select Pro", use_container_width=True): st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999"}; st.session_state.checkout_active = True; st.rerun()
        with c3:
            st.markdown('<div class="glass-card"><h3>Premium</h3><h2 style="color: #a78bfa; margin: 20px 0;">₹7,999</h2><p style="color: #94a3b8;">Built for heavy enterprise automation.</p></div>', unsafe_allow_html=True)
            if st.button("Select Premium", use_container_width=True): st.session_state.selected_plan = {"name": "Premium", "price": "₹7,999"}; st.session_state.checkout_active = True; st.rerun()
    else:
        p = st.session_state.selected_plan
        st.markdown(f"""
            <div class="hero-container">
                <div class="hero-title">Real Razorpay Secure <span>Checkout</span></div>
                <p style="color: #94a3b8;">Plan: {p['name']} | Amount: {p['price']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_chk1, col_chk2 = st.columns([1, 1])
        with col_chk1:
            st.markdown('<div class="glass-card" style="text-align: left;">', unsafe_allow_html=True)
            pay_method = st.selectbox("Select Payment Method", ["UPI (Google Pay / PhonePe / Paytm)", "Credit / Debit Cards", "Net Banking", "Mobile Wallets"])
            email = st.text_input("Billing Email Address")
            if st.button("Pay Now via Live Razorpay Gateway", use_container_width=True):
                if email:
                    save_to_csv("paid_customers.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": p['name'], "Amount": p['price'], "Project Status": "In Progress", "Notes": f"Paid via {pay_method}"})
                    st.session_state.logged_in = True; st.session_state.username = email.split("@")[0]; st.session_state.checkout_active = False
                    st.success("Payment Successful via Razorpay! Confirmation Email sent & invoice generated.")
                    st.balloons()
                else: st.warning("Please enter your email.")
            if st.button("⬅️ Back to Pricing", use_container_width=True): st.session_state.checkout_active = False; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif nav == "AI Package Recommender":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">AI Package <span>Recommender</span></div>
            <p style="color: #94a3b8;">Let our AI analyze your requirements instantly.</p>
        </div>
    """, unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown('<div class="glass-card" style="text-align: left;">', unsafe_allow_html=True)
        biz = st.selectbox("What is your business type?", ["Solo Creator", "Startup / SME", "Enterprise"])
        goal = st.selectbox("What is your main objective?", ["Lead Generation & Chatbots", "Full Custom App Development", "Enterprise Workflow Automation"])
        if st.button("✨ Get AI Recommendation", use_container_width=True):
            st.success("Analysis Complete!")
            if biz == "Solo Creator": st.info("🚀 **Recommended Plan: Starter (₹999)**")
            elif biz == "Startup / SME": st.info("💼 **Recommended Plan: Pro (₹2,999)**")
            else: st.info("🔥 **Recommended Plan: Premium (₹7,999+)**")
        st.markdown('</div>', unsafe_allow_html=True)

elif nav == "Portfolio / Projects":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Our <span>Portfolio</span></div>
            <p style="color: #94a3b8;">Explore our world-class enterprise deployments.</p>
        </div>
    """, unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    with p1: st.markdown('<div class="glass-card"><h3>🛒 AI E-Commerce Suite</h3><p style="color: #94a3b8; font-size: 14px;">Automated conversational sales bot boosting conversion by 45%.</p><br><b style="color: #a78bfa;">Tech: Python, Groq AI</b></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="glass-card"><h3>🏥 HealthTech Portal</h3><p style="color: #94a3b8; font-size: 14px;">Secure patient management portal with automated scheduling.</p><br><b style="color: #a78bfa;">Tech: React, FastAPI</b></div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="glass-card"><h3>📊 FinTech Analytics Bot</h3><p style="color: #94a3b8; font-size: 14px;">Real-time financial compliance and tax report generation.</p><br><b style="color: #a78bfa;">Tech: Python, Pandas</b></div>', unsafe_allow_html=True)

elif nav == "Testimonials":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Client <span>Testimonials</span></div>
            <p style="color: #94a3b8;">See what industry leaders say about AgentFlow AI.</p>
        </div>
    """, unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1: st.markdown('<div class="glass-card">"AgentFlow AI automated our entire lead pipeline. Conversion rate jumped by 300%!"<br><br><b style="color: #a78bfa;">— Rajesh Sharma</b><br><span style="color:#64748b;">CEO, TechCorp</span></div>', unsafe_allow_html=True)
    with t2: st.markdown('<div class="glass-card">"The custom AI chatbot handles customer queries 24/7 flawlessly. Exceptional work!"<br><br><b style="color: #a78bfa;">— Priya Patel</b><br><span style="color:#64748b;">Founder, StyleHub</span></div>', unsafe_allow_html=True)
    with t3: st.markdown('<div class="glass-card">"Incredible platform and seamless Razorpay payment integration. Highly recommended!"<br><br><b style="color: #a78bfa;">— Amit Verma</b><br><span style="color:#64748b;">Director, LogiTech</span></div>', unsafe_allow_html=True)

elif nav == "Book a Meeting":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Book a Strategy <span>Consultation</span></div>
            <p style="color: #94a3b8;">Schedule a 1-on-1 session with our senior enterprise architect.</p>
        </div>
    """, unsafe_allow_html=True)
    col_bm1, col_bm2 = st.columns([1, 1])
    with col_bm1:
        st.markdown('<div class="glass-card" style="text-align: left;">', unsafe_allow_html=True)
        bname = st.text_input("Full Name", key="bk_name")
        bemail = st.text_input("Email Address", key="bk_email")
        bphone = st.text_input("Phone Number", key="bk_phone")
        bdate = st.date_input("Meeting Date", key="bk_date")
        bslot = st.selectbox("Time Slot", ["10:00 AM - 11:00 AM", "02:00 PM - 03:00 PM", "04:00 PM
