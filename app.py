import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Premium Enterprise SaaS", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# World-Class Premium SaaS CSS (Sticky Navbar, Glassmorphism, Pure White/Dark Theme, Smooth Gradients)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Poppins', sans-serif;
        background-color: #030712;
        color: #FFFFFF;
    }

    /* Hide standard sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Sticky Transparent Navbar */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 99999;
        background: rgba(3, 7, 18, 0.8);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding: 16px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-logo {
        font-size: 20px;
        font-weight: 800;
        color: #FFFFFF;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Full-Screen Hero Section with Gradients */
    .hero-section {
        min-height: 90vh;
        display: flex;
        align-items: center;
        padding: 120px 20px 60px 20px;
        background: radial-gradient(circle at 70% 30%, rgba(124, 58, 237, 0.15) 0%, rgba(59, 130, 246, 0.1) 40%, transparent 70%);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 32px;
        text-align: left;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 30px 60px rgba(124, 58, 237, 0.2);
    }

    /* Floating WhatsApp Button */
    .whatsapp-float {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white;
        border-radius: 50px;
        text-align: center;
        font-size: 26px;
        box-shadow: 0 10px 25px rgba(37, 211, 102, 0.4);
        z-index: 10000;
        width: 55px;
        height: 55px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
    }

    .footer {
        background: #030712;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 60px 40px 30px 40px;
        margin-top: 80px;
    }
</style>

<!-- Sticky Transparent Navbar HTML -->
<div class="nav-container">
    <div class="nav-logo">⚡ AgentFlow AI</div>
    <div style="color: #94A3B8; font-size: 14px;">Enterprise AI & Business Automation Platform</div>
</div>

<a href="https://wa.me/919876543210" class="whatsapp-float" target="_blank" title="Chat on WhatsApp">💬</a>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Collect 6 details: Name, Business Name, Service Required, Budget, Phone Number, Email Address. When collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! Welcome to AgentFlow AI. What is your name?"})

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
    Amount Paid: {amount}
    Status: SUCCESSFUL / VERIFIED
    -----------------------------------
    Thank you for your business!
    """

# ==================== HERO SECTION ====================
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
col_h1, col_h2 = st.columns([1.2, 1], gap="large")

with col_h1:
    st.markdown("""
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #FFFFFF; font-weight: 600; font-size: 13px; padding: 6px 16px; border-radius: 50px; margin-bottom: 20px;">
            ✨ Next-Gen Enterprise AI & Automation
        </div>
        <h1 style="font-size: 56px; font-weight: 800; color: #FFFFFF; line-height: 1.15; margin-bottom: 20px;">
            Scale Your Business with AgentFlow AI
        </h1>
        <p style="font-size: 18px; color: #94A3B8; line-height: 1.6; margin-bottom: 35px;">
            AI Chatbots, Websites, Mobile Apps & Business Automation for Modern Companies.
        </p>
    """, unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)
    with ch1:
        if st.button("🚀 Get Started", use_container_width=True):
            st.balloons()
    with ch2:
        if st.button("📅 Book Demo", use_container_width=True):
            st.info("Scroll down to the Contact & Booking section below.")

with col_h2:
    st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 50px 30px; background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);">
            <h2 style="font-size: 64px; margin-bottom: 15px;">🤖⚡</h2>
            <h3 style="color: #FFFFFF; margin-bottom: 10px;">Futuristic AI Dashboard</h3>
            <p style="font-size: 14px; color: #94A3B8;">Autonomous agents analyzing pipelines and optimizing conversion rates 24/7.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== TRUST SECTION ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 40px; color: #FFFFFF;'>Trusted by Industry Leaders Worldwide</h2>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.columns(4)
with t1: st.markdown('<div class="glass-card" style="text-align: center;"><h2 style="color: #FFFFFF; font-size: 38px; margin-bottom: 5px;">100+</h2><p style="color: #94A3B8;">Clients</p></div>', unsafe_allow_html=True)
with t2: st.markdown('<div class="glass-card" style="text-align: center;"><h2 style="color: #FFFFFF; font-size: 38px; margin-bottom: 5px;">500+</h2><p style="color: #94A3B8;">Projects</p></div>', unsafe_allow_html=True)
with t3: st.markdown('<div class="glass-card" style="text-align: center;"><h2 style="color: #FFFFFF; font-size: 38px; margin-bottom: 5px;">99%</h2><p style="color: #94A3B8;">Satisfaction</p></div>', unsafe_allow_html=True)
with t4: st.markdown('<div class="glass-card" style="text-align: center;"><h2 style="color: #FFFFFF; font-size: 38px; margin-bottom: 5px;">24/7</h2><p style="color: #94A3B8;">Support</p></div>', unsafe_allow_html=True)

# ==================== SERVICES ====================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 10px; color: #FFFFFF;'>Our Core Services</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Comprehensive digital and artificial intelligence solutions designed for scale.</p>", unsafe_allow_html=True)

srv1, srv2, srv3, srv4 = st.columns(4)
with srv1: st.markdown('<div class="glass-card"><h3>🤖 AI Chatbots</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Intelligent customer support and sales conversion bots.</p></div>', unsafe_allow_html=True)
with srv2: st.markdown('<div class="glass-card"><h3>🎙️ AI Voice Agents</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Human-like voice assistants for phone calls and inquiries.</p></div>', unsafe_allow_html=True)
with srv3: st.markdown('<div class="glass-card"><h3>🌐 Website Development</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Lightning-fast, high-converting modern web applications.</p></div>', unsafe_allow_html=True)
with srv4: st.markdown('<div class="glass-card"><h3>📱 Mobile Apps</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Scalable iOS & Android apps built for performance.</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
srv5, srv6, srv7, srv8 = st.columns(4)
with srv5: st.markdown('<div class="glass-card"><h3>💬 WhatsApp Automation</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Automate messaging, broadcasts, and lead routing.</p></div>', unsafe_allow_html=True)
with srv6: st.markdown('<div class="glass-card"><h3>📊 CRM Automation</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Seamless pipeline management and data synchronization.</p></div>', unsafe_allow_html=True)
with srv7: st.markdown('<div class="glass-card"><h3>⚡ AI Integrations</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Custom LLM embeddings and intelligent workflows.</p></div>', unsafe_allow_html=True)
with srv8: st.markdown('<div class="glass-card"><h3>🎨 UI/UX Design</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">World-class user interfaces crafted for maximum engagement.</p></div>', unsafe_allow_html=True)

# ==================== PORTFOLIO ====================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 10px; color: #FFFFFF;'>Featured Portfolio</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Explore our successful enterprise deployments.</p>", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)
with p1: st.markdown('<div class="glass-card"><h3>🛒 AI E-Commerce Suite</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Automated conversational sales bot boosting conversions by 45%.</p><br><b style="color: #FFFFFF;">Tech: Python, Groq AI</b></div>', unsafe_allow_html=True)
with p2: st.markdown('<div class="glass-card"><h3>🏥 HealthTech Portal</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Secure patient management portal with automated scheduling.</p><br><b style="color: #FFFFFF;">Tech: React, FastAPI</b></div>', unsafe_allow_html=True)
with p3: st.markdown('<div class="glass-card"><h3>📊 FinTech Analytics Bot</h3><p style="color: #94A3B8; font-size: 14px; margin-top: 10px;">Real-time financial compliance and tax report generation.</p><br><b style="color: #FFFFFF;">Tech: Python, Pandas</b></div>', unsafe_allow_html=True)

# ==================== TESTIMONIALS ====================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 10px; color: #FFFFFF;'>Client Testimonials</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Hear what founders and industry leaders say about AgentFlow AI.</p>", unsafe_allow_html=True)

ts1, ts2, ts3 = st.columns(3)
with ts1: st.markdown('<div class="glass-card">"AgentFlow AI automated our entire lead pipeline. Conversion rate jumped by 300%!"<br><br><b style="color: #FFFFFF;">— Rajesh Sharma</b><br><span style="color:#94A3B8; font-size: 13px;">CEO, TechCorp</span></div>', unsafe_allow_html=True)
with ts2: st.markdown('<div class="glass-card">"The custom AI chatbot handles customer queries 24/7 flawlessly. Exceptional work!"<br><br><b style="color: #FFFFFF;">— Priya Patel</b><br><span style="color:#94A3B8; font-size: 13px;">Founder, StyleHub</span></div>', unsafe_allow_html=True)
with ts3: st.markdown('<div class="glass-card">"Incredible platform and seamless Razorpay payment integration. Highly recommended!"<br><br><b style="color: #FFFFFF;">— Amit Verma</b><br><span style="color:#94A3B8; font-size: 13px;">Director, LogiTech</span></div>', unsafe_allow_html=True)

# ==================== PRICING ====================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 10px; color: #FFFFFF;'>Transparent Pricing Plans</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Choose the ideal tier with instant Razorpay checkout.</p>", unsafe_allow_html=True)

if not st.session_state.checkout_active:
    pr1, pr2, pr3 = st.columns(3)
    with pr1:
        st.markdown('<div class="glass-card"><h3>Starter</h3><h2 style="color: #FFFFFF; margin: 20px 0;">₹999</h2><p style="color: #94A3B8;">Ideal for solo creators & small tasks.</p></div>', unsafe_allow_html=True)
        if st.button("Select Starter", use_container_width=True, key="btn_st"): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
    with pr2:
        st.markdown('<div class="glass-card" style="border-color: rgba(124, 58, 237, 0.5);"><h3>Business</h3><h2 style="color: #FFFFFF; margin: 20px 0;">₹4,999</h2><p style="color: #94A3B8;">For growing businesses & automated scaling.</p></div>', unsafe_allow_html=True)
        if st.button("Select Business", use_container_width=True, key="btn_bs"): st.session_state.selected_plan = {"name": "Business", "price": "₹4,999"}; st.session_state.checkout_active = True; st.rerun()
    with pr3:
        st.markdown('<div class="glass-card"><h3>Enterprise</h3><h2 style="color: #FFFFFF; margin: 20px 0;">Custom</h2><p style="color: #94A3B8;">Tailored solutions for large organizations.</p></div>', unsafe_allow_html=True)
        if st.button("Contact Sales", use_container_width=True, key="btn_en"): st.info("Reach out via our contact section below.")
else:
    p = st.session_state.selected_plan
    col_chk1, col_chk2 = st.columns([1, 1])
    with col_chk1:
        st.markdown(f'<div class="glass-card"><h3>Razorpay Secure Checkout</h3><p style="color: #94A3B8; margin: 15px 0;">Plan: <b>{p["name"]}</b> | Amount: <b>{p["price"]}</b></p>', unsafe_allow_html=True)
        pay_method = st.selectbox("Select Payment Method", ["UPI (Google Pay / PhonePe / Paytm)", "Credit / Debit Cards", "Net Banking", "Mobile Wallets"])
        email = st.text_input("Billing Email Address")
        if st.button("Pay Now via Live Razorpay Gateway", use_container_width=True):
            if email:
                save_to_csv("paid_customers.csv", {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": p['name'], "Amount": p['price'], "Project Status": "In Progress", "Notes": f"Paid via {pay_method}"})
                st.session_state.checkout_active = False
                st.success("Payment Successful via Razorpay! Confirmation & invoice generated.")
                st.balloons()
            else: st.warning("Please enter your email.")
        if st.button("⬅️ Back to Pricing", use_container_width=True): st.session_state.checkout_active = False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FAQ ====================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 10px; color: #FFFFFF;'>Frequently Asked Questions</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Everything you need to know about the product and billing.</p>", unsafe_allow_html=True)

col_faq1, col_faq2 = st.columns(2)
with col_faq1:
    with st.expander("How quickly can my AI chatbot be deployed?"):
        st.write("Most chatbots are fully deployed and integrated into your workflow within 24 to 48 hours.")
    with st.expander("Are payments secure with Razorpay?"):
        st.write("Yes! All transactions are encrypted and processed securely through Razorpay supporting UPI, cards, and wallets.")
with col_faq2:
    with st.expander("Can I upgrade or downgrade my plan?"):
        st.write("You can upgrade or modify your subscription tier at any time directly through your dashboard or by contacting support.")
    with st.expander("Do you offer custom enterprise solutions?"):
        st.write("Yes, our Enterprise tier includes dedicated server hosting, custom LLM embeddings, and 24/7 priority support.")

# ==================== CONTACT & BOOKING ====================
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 10px; color: #FFFFFF;'>Contact & Book Meeting</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 40px;'>Connect with our team or schedule a strategy consultation.</p>", unsafe_allow_html=True)

con1, con2 = st.columns(2, gap="large")
with con1:
    st.markdown("""
        <div class="glass-card">
            <h3>Get in Touch</h3>
            <p style="color: #94A3B8; margin: 15px 0 25px 0;">Reach out through any of our official channels:</p>
            <p style="margin-bottom: 10px;">💬 <b>WhatsApp:</b> +91 98765 43210</p>
            <p style="margin-bottom: 10px;">📧 <b>Email:</b> support@agentflow.ai</p>
            <p style="margin-bottom: 10px;">📞 <b>Phone:</b> +91 98765 43210</p>
        </div>
    """, unsafe_allow_html=True)

with con2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Book Meeting Form")
    bname = st.text_input("Full Name", key="bk_name")
    bemail = st.text_input("Email Address", key="bk_email")
    bphone = st.text_input("Phone Number", key="bk_phone")
    bdate = st.date_input("Meeting Date", key="bk_date")
    bslot = st.selectbox("Time Slot", ["10:00 AM - 11:00 AM", "02:00 PM - 03:00 PM", "04:00 PM - 05:00 PM"])
    if st.button("Confirm Meeting Booking", use_container_width=True):
        if bname and bemail:
            save_to_csv("bookings.csv", {"Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer Name": bname, "Email": bemail, "Phone": bphone, "Service": "Consultation", "Meeting Date": str(bdate), "Time Slot": bslot, "Status": "Pending", "Notes": "Booked"})
            st.success("Meeting booked successfully! Admin notified.")
        else: st.warning("Please fill in required details.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px; max-width: 1200px; margin: 0 auto;">
            <div>
                <h3>⚡ AgentFlow AI</h3>
                <p style="color: #94A3B8; font-size: 14px; max-width: 300px; margin-top: 10px;">Enterprise-grade AI automation and software development solutions.</p>
            </div>
            <div>
                <h4>Legal & Policies</h4>
                <p style="color: #94A3B8; font-size: 14px; margin-top: 8px;">🔒 Privacy Policy</p>
                <p style="color: #94A3B8; font-size: 14px;">📜 Terms & Conditions</p>
                <p style="color: #94A3B8; font-size: 14
