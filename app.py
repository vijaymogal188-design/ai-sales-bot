import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS & Business Automation Portal", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        animation: fadeIn 0.6s ease-out;
    }

    .hero-container {
        text-align: center;
        padding: 40px 20px 20px 20px;
        max-width: 900px;
        margin: 0 auto;
    }
    .hero-badge {
        display: inline-block;
        background: #ede9fe;
        color: #7c3aed;
        font-weight: 700;
        font-size: 13px;
        padding: 6px 16px;
        border-radius: 50px;
        margin-bottom: 16px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
        margin-bottom: 16px;
    }
    .hero-title span {
        background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 25px;
    }
    .section-title {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 50px;
        margin-bottom: 10px;
    }
    .section-subtitle {
        text-align: center;
        font-size: 15px;
        color: #64748b;
        margin-bottom: 30px;
    }
    .pricing-card, .feature-card, .testimonial-card, .portfolio-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .pricing-card:hover, .feature-card:hover, .testimonial-card:hover, .portfolio-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.1);
    }
    .checkout-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 30px;
        border-radius: 16px;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .trust-badge-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 40px 0;
        flex-wrap: wrap;
    }
    .trust-badge {
        background: #f1f5f9;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        color: #334155;
        border: 1px solid #cbd5e1;
    }
    .footer {
        background: #0f172a;
        color: #f8fafc;
        padding: 50px 30px 20px 30px;
        border-top: 1px solid #1e293b;
        margin-top: 60px;
        border-radius: 16px 16px 0 0;
    }
    .footer a {
        color: #94a3b8;
        text-decoration: none;
    }
    .footer a:hover {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. You can converse in both English and Hindi (or Hinglish) depending on user preference. Your goal is to naturally converse with the user and collect exactly these 6 details:
1. Name
2. Business Name
3. Service Required
4. Budget
5. Phone Number
6. Email Address

RULES:
- Match user's language (English/Hindi).
- Ask conversationally, one or two details at a time.
- Once ALL 6 details are collected, output EXACTLY this format and nothing else:
COMPLETE: Name | Business | Service | Budget | Phone | Email
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "👋 Hello! Welcome to AgentFlow AI. To get started, could you please tell me your name?"
    })

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = None
if "checkout_active" not in st.session_state:
    st.session_state.checkout_active = False

def save_lead_to_csv(data_list):
    file_name = "leads.csv"
    new_lead = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": data_list[0].strip(),
        "Business": data_list[1].strip(),
        "Service": data_list[2].strip(),
        "Budget": data_list[3].strip(),
        "Phone": data_list[4].strip(),
        "Email": data_list[5].strip()
    }
    df = pd.DataFrame([new_lead])
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, mode='a', header=False, index=False)

def save_paid_customer(email, plan_name, amount):
    file_name = "paid_customers.csv"
    record = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Email": email,
        "Plan": plan_name,
        "Amount": amount
    }
    df = pd.DataFrame([record])
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, mode='a', header=False, index=False)

st.sidebar.markdown("### ⚡ AgentFlow Portal")
st.sidebar.markdown("🟢 **Live Visitors Online:** `142 active`")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio("Navigation", [
    "Home / Landing Page", 
    "Pricing & Plans", 
    "About Us", 
    "Portfolio / Projects", 
    "Contact Us", 
    "FAQ", 
    "Customer Login / Signup", 
    "Admin Portal",
    "Legal & Policies"
])

st.sidebar.markdown("---")
st.sidebar.markdown("🛡️ **Enterprise Security**")
st.sidebar.caption("SSL Secured | 24/7 Support | Verified Gateway")

if nav_choice == "Home / Landing Page":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">⚡ Next-Gen Business Automation & AI</div>
            <div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div>
            <div class="hero-subtitle">Experience lightning-fast client acquisition, intelligent workflow automations, and bespoke digital solutions designed to elevate your brand globally.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="trust-badge-container">
            <div class="trust-badge">🔒 100% Secure Payment</div>
            <div class="trust-badge">🛠️ 24/7 Expert Support</div>
            <div class="trust-badge">🔐 Enterprise SSL Secured</div>
            <div class="trust-badge">⚡ 99.9% Uptime Guarantee</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="section-title">Our Professional Services</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-subtitle">Comprehensive solutions tailored to scale your digital presence.</div>""", unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1:
        st.markdown('<div class="feature-card"><h3>🌐 Website Dev</h3><p>High-performing modern responsive websites.</p></div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown('<div class="feature-card"><h3>🤖 AI Chatbots</h3><p>24/7 intelligent sales conversational bots.</p></div>', unsafe_allow_html=True)
    with col_s3:
        st.markdown('<div class="feature-card"><h3>📱 App Dev</h3><p>Scalable mobile apps for iOS & Android.</p></div>', unsafe_allow_html=True)
    with col_s4:
        st.markdown('<div class="feature-card"><h3>🎨 Logo Design</h3><p>Memorable brand identities & graphics.</p></div>', unsafe_allow_html=True)
    with col_s5:
        st.markdown('<div class="feature-card"><h3>📈 Marketing</h3><p>Data-driven customer growth campaigns.</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""<div class="section-title">⭐ What Our Clients Say</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-subtitle">Trusted by hundreds of forward-thinking founders and enterprises.</div>""", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown('<div class="testimonial-card">"AgentFlow AI automated our entire lead pipeline. Our conversion rate jumped by 300% in just two weeks!"<br><br><b>— Rajesh Sharma</b><br><span style="color: #64748b; font-size: 13px;">CEO, TechCorp India</span></div>', unsafe_allow_html=True)
    with t2:
        st.markdown('<div class="testimonial-card">"The custom AI chatbot built for our e-commerce store handles customer queries flawlessly 24/7. Exceptional work!"<br><br><b>— Priya Patel</b><br><span style="color: #64748b; font-size: 13px;">Founder, StyleHub</span></div>', unsafe_allow_html=True)
    with t3:
        st.markdown('<div class="testimonial-card">"Incredible platform and seamless payment onboarding. The dashboard gives us absolute clarity on our projects."<br><br><b>— Amit Verma</b><br><span style="color: #64748b; font-size: 13px;">Director, LogiTech Solutions</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""<div class="section-title">💬 Interactive AI Sales Assistant</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-subtitle">Chat with our assistant below to share your custom requirements.</div>""", unsafe_allow_html=True)

    col_c1, col_chat, col_c3 = st.columns([1, 2.5, 1])
    with col_chat:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Type your message here..."):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.1-8b-instant",
                        temperature=0.5
                    )
                    response_text = chat_completion.choices[0].message.content
                    
                    if "COMPLETE:" in response_text:
                        data_part = response_text.split("COMPLETE:")[1].strip()
                        lead_data = data_part.split("|")
                        if len(lead_data) == 6:
                            save_lead_to_csv(lead_data)
                        final_msg = "Thank you! Your details have been received. Our team will contact you soon."
                        st.markdown(final_msg)
                        st.session_state.messages.append({"role": "assistant", "content": final_msg})
                    else:
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    st.markdown("""
        <div class="footer">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px; max-width: 1200px; margin: 0 auto;">
                <div>
                    <h3>⚡ AgentFlow AI</h3>
                    <p style="color: #94a3b8; font-size: 14px; max-width: 300px;">Enterprise-grade AI automation and software development solutions for scaling modern businesses globally.</p>
                </div>
                <div>
                    <h4>Quick Links</h4>
                    <p><a href="#">About Us</a></p>
                    <p><a href="#">Pricing Plans</a></p>
                    <p><a href="#">Portfolio</a></p>
                    <p><a href="#">Contact Support</a></p>
                </div>
                <div>
                    <h4>Contact Desk</h4>
                    <p style="color: #94a3b8; font-size: 14px;">📧 Email: support@agentflow.ai</p>
                    <p style="color: #94a3b8; font-size: 14px;">💬 WhatsApp: +91 98765 43210</p>
                    <p style="color: #94a3b8; font-size: 14px;">📍 Location: Tech Hub, Bangalore, India</p>
                </div>
            </div>
            <div style="text-align: center; border-top: 1px solid #1e293b; margin-top: 40px; padding-top: 20px; color: #64748b; font-size: 14px;">
                <p>© 2026 AgentFlow AI. All rights reserved. Built with advanced AI & Streamlit.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif nav_choice == "Pricing & Plans":
    if not st.session_state.checkout_active:
        st.markdown("""<div class="section-title">Choose Your Growth Plan</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="section-subtitle">Select a plan to proceed with secure Razorpay checkout supporting UPI, Cards, Net Banking & Wallets.</div>""", unsafe_allow_html=True)

        col_p1, col_p2, col_p3, col_p4 = st.columns(4)

        with col_p1:
            st.markdown("""
                <div class="pricing-card">
                    <h3>🚀 Starter</h3>
                    <h2>₹999</h2>
                    <p>Ideal for solo creators and small projects.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select Starter", key="sel_starter"):
                st.session_state.selected_plan = {"name": "Starter", "price": "₹999", "amount": 999}
                st.session_state.checkout_active = True
                st.rerun()

        with col_p2:
            st.markdown("""
                <div class="pricing-card" style="border: 2px solid #7c3aed;">
                    <h3>💼 Pro</h3>
                    <h2>₹2,999</h2>
                    <p>Great for growing businesses looking for automation.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select Pro", key="sel_pro"):
                st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999", "amount": 2999}
                st.session_state.checkout_active = True
                st.rerun()

        with col_p3:
            st.markdown("""
                <div class="pricing-card">
                    <h3>🔥 Premium</h3>
                    <h2>₹7,999</h2>
                    <p>Advanced capabilities for scaling agencies & enterprises.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Select Premium", key="sel_premium"):
                st.session_state.selected_plan = {"name": "Premium", "price": "₹7,999", "amount": 7999}
                st.session_state.checkout_active = True
                st.rerun()

        with col_p4:
            st.markdown("""
                <div class="pricing-card">
                    <h3>🏢 Enterprise</h3>
                    <h2>Contact Sales</h2>
                    <p>Tailored infrastructure and custom workflows.</p>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            st.write("")
            if st.button("Contact Sales"):
                st.info("Please reach out via our support desk for custom enterprise integrations.")
    
    else:
        plan = st.session_state.selected_plan
        st.markdown(f"<h2 style='text-align: center;'>🔒 Secure Checkout - {plan['name']} Plan</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Powered by Razorpay Secure Gateway (UPI, Cards, NetBanking, Wallets)</p>", unsafe_allow_html=True)
        
        st.write("")
        col_c1, col_box, col_c3 = st.columns([1, 2, 1])
        with col_box:
            st.markdown("""
                <div class="checkout-box">
                    <h3>📋 Order Summary</h3>
            """, unsafe_allow_html=True)
            st.write(f"**Plan Tier:** {plan['name']} Subscription")
            st.write(f"**Billing Cycle:** Monthly / Instant Access")
            st.write(f"**Total Amount:** {plan['price']}")
            st.markdown("---")
            
            customer_email = st.text_input("Billing Email Address (Account will be created here)")
            
            if st.button("Simulate Secure Razorpay Payment & Complete Order"):
                if customer_email:
                    save_paid_customer(customer_email, plan['name'], plan['price'])
                    st.session_state.logged_in = True
                    st.session_state.username = customer_email.split("@")[0]
                    st.session_state.checkout_active = False
                    st.success("Payment Successful via Razorpay! Account & Invoice generated automatically. Redirecting to Dashboard...")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("Please enter your billing email address first.")
            
            if st.button("⬅️ Back to Pricing Plans"):
                st.session_state.checkout_active = False
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)

elif nav_choice == "About Us":
    st.markdown("""<div class="section-title">About AgentFlow AI</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-subtitle">Empowering businesses through cutting-edge artificial intelligence and workflow automation.</div>""", unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("### 🚀 Our Mission")
        st.write("At AgentFlow AI, our mission is to bridge the gap between complex enterprise technology and everyday business efficiency. We build lightning-fast AI sales agents, automated workflows, and robust digital ecosystems that allow businesses to scale effortlessly without ballooning overheads.")
        st.markdown("### 💡 Why Choose Us?")
        st.markdown("- **State-of-the-Art AI:** Powered by advanced large language models for human-like conversations.")
        st.markdown("- **Enterprise Reliability:** 99.9% uptime with bank-grade security and encryption.")
        st.markdown("- **Dedicated Support:** 24/7 technical and customer success assistance.")
    with col_a2:
        st.markdown("### 📈 Our Impact in Numbers")
        st.metric(label="Active Business Clients", value="1,200+", delta="+18% this month")
        st.metric(label="Automated Leads Processed", value="450,000+", delta="99.4% Success Rate")
        st.metric(label="Global Team Members", value="45+", delta="Expert Engineers & AI Researchers")

elif nav_choice == "Portfolio / Projects":
    st.markdown("""<div class="section-title">Our Portfolio & Previous Projects</div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-subtitle">A showcase of successful digital transformations and enterprise deployments.</div>""", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown('<div class="portfolio-card"><h3>🛒 AI E-Commerce Suite</h3><p>Built an automated conversational sales bot and inventory tracker for a major retail brand, boosting sales by 45%.</p><br><b>Tech:</b> Python, Groq AI, Streamlit</div>', unsafe_allow_html=True)
    with p2:
        st.markdown('<div class="portfolio-card"><h3>🏥 HealthTech SaaS Portal</h3><p>Developed a secure patient management dashboard with automated appointment scheduling and billi
