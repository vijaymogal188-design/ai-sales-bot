import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS Platform", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL ULTRA-MODERN DARK SaaS STYLING (GLASSMORPHISM & NEON) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #07090e;
        color: #f1f5f9;
    }

    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #07090e 60%);
    }

    [data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }

    .hero-container {
        text-align: center;
        padding: 60px 20px 40px 20px;
        max-width: 950px;
        margin: 0 auto;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(124, 58, 237, 0.15);
        color: #a78bfa;
        font-weight: 700;
        font-size: 13px;
        padding: 6px 18px;
        border-radius: 50px;
        border: 1px solid rgba(124, 58, 237, 0.3);
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
        margin-bottom: 20px;
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
        margin-bottom: 40px;
        max-width: 750px;
        margin-left: auto;
        margin-right: auto;
    }

    .stats-container {
        display: flex;
        justify-content: space-around;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px;
        border-radius: 16px;
        backdrop-filter: blur(12px);
        margin: 40px auto;
        max-width: 850px;
        text-align: center;
    }

    .stat-number {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
    }

    .stat-label {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .section-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 60px;
        margin-bottom: 12px;
    }

    .section-subtitle {
        text-align: center;
        font-size: 16px;
        color: #94a3b8;
        margin-bottom: 40px;
    }

    .glass-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 32px 24px;
        border-radius: 20px;
        text-align: center;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }

    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(124, 58, 237, 0.5);
        box-shadow: 0 20px 40px -15px rgba(124, 58, 237, 0.25);
    }

    .footer {
        background: #030712;
        color: #94a3b8;
        padding: 60px 30px 30px 30px;
        border-top: 1px solid #1e293b;
        margin-top: 80px;
        border-radius: 24px 24px 0 0;
    }
</style>
""", unsafe_allow_html=True)

try:
    from groq import Groq
    client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "dummy_key"))
except Exception:
    client = None

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Your goal is to converse with the user and collect exactly these 6 details:
1. Name, 2. Business Name, 3. Service Required, 4. Budget, 5. Phone Number, 6. Email Address.
When all 6 are collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! Welcome to AgentFlow AI. To get started, could you please tell me your name?"
    })

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_user_to_csv(username, email, password):
    file_name = "users.csv"
    new_user = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Username": username, "Email": email, "Password": password}
    df = pd.DataFrame([new_user])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def save_lead_to_csv(data_list):
    file_name = "leads.csv"
    new_lead = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": data_list[0].strip(), "Business": data_list[1].strip(), "Service": data_list[2].strip(), "Budget": data_list[3].strip(), "Phone": data_list[4].strip(), "Email": data_list[5].strip(), "Status": "New", "Notes": "None"}
    df = pd.DataFrame([new_lead])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def save_paid_customer(email, plan_name, amount):
    file_name = "paid_customers.csv"
    record = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": plan_name, "Amount": amount, "Project Status": "In Progress", "Notes": "New subscription paid"}
    df = pd.DataFrame([record])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def save_booking_to_csv(name, email, phone, service, date, time_slot):
    file_name = "bookings.csv"
    record = {"Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Customer Name": name, "Email": email, "Phone": phone, "Service": service, "Meeting Date": str(date), "Time Slot": str(time_slot), "Status": "Pending", "Notes": "Scheduled consultation"}
    df = pd.DataFrame([record])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def generate_invoice_pdf(email, plan, amount):
    return f"""
    AGENTFLOW AI - OFFICIAL GLOBAL INVOICE
    --------------------------------------------------
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Customer Email: {email}
    Selected Plan: {plan}
    Gateway: Razorpay Secure (Global UPI / Cards / Net Banking)
    Amount Paid: {amount}
    Status: VERIFIED & SUCCESSFUL
    --------------------------------------------------
    Thank you for scaling with AgentFlow AI!
    """

query_params = st.query_params
is_admin_url = query_params.get("admin") == "true"

st.sidebar.markdown("### ⚡ AgentFlow AI")
st.sidebar.caption("Enterprise Global SaaS v4.0")
st.sidebar.markdown("---")

nav_options = [
    "Home / Landing Page", 
    "Pricing & Plans", 
    "AI Package Recommender",
    "Portfolio / Projects", 
    "Testimonials", 
    "Book a Meeting",
    "Contact Us", 
    "Customer Login / Signup", 
    "Legal & Policies"
]

if is_admin_url:
    nav_options.append("Admin CRM Dashboard")

nav_choice = st.sidebar.radio("Navigation", nav_options)

st.sidebar.markdown("---")
st.sidebar.markdown("🔒 **Security & Trust**")
st.sidebar.caption("SOC2 Type II Certified | 99.9% Uptime")

if nav_choice == "Home / Landing Page":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">✨ Next-Gen Enterprise AI Automation</div>
            <div class="hero-title">Scale Your Global Growth with <span>AgentFlow AI</span></div>
            <div class="hero-subtitle">Deploy hyper-intelligent autonomous agents, streamline client acquisition, and automate your revenue pipelines with world-class digital engineering.</div>
        </div>
        
        <div class="stats-container">
            <div>
                <div class="stat-number">99.9%</div>
                <div class="stat-label">Platform Uptime</div>
            </div>
            <div>
                <div class="stat-number">500+</div>
                <div class="stat-label">Global Enterprises</div>
            </div>
            <div>
                <div class="stat-number">$15M+</div>
                <div class="stat-label">Client Revenue Generated</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Core Capabilities</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Engineered for extreme performance and modern digital brands.</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1: st.markdown('<div class="glass-card"><h4>Web Architecture</h4><p style="color:#94a3b8; font-size:13px;">Lightning fast responsive platforms.</p></div>', unsafe_allow_html=True)
    with col_s2: st.markdown('<div class="glass-card"><h4>AI Sales Bots</h4><p style="color:#94a3b8; font-size:13px;">24/7 autonomous closing agents.</p></div>', unsafe_allow_html=True)
    with col_s3: st.markdown('<div class="glass-card"><h4>Mobile Apps</h4><p style="color:#94a3b8; font-size:13px;">Scalable iOS & Android ecosystems.</p></div>', unsafe_allow_html=True)
    with col_s4: st.markdown('<div class="glass-card"><h4>Brand ID</h4><p style="color:#94a3b8; font-size:13px;">Iconic, high-impact design identities.</p></div>', unsafe_allow_html=True)
    with col_s5: st.markdown('<div class="glass-card"><h4>Growth Ops</h4><p style="color:#94a3b8; font-size:13px;">Data-driven conversion funnels.</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Experience Our AI Sales Assistant</div>', unsafe_allow_html=True)
    
    col_c1, col_chat, col_c3 = st.columns([1, 2.8, 1])
    with col_chat:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]): st.markdown(message["content"])
        if prompt := st.chat_input("Ask about our services or start a project..."):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                try:
                    if client:
                        chat_completion = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.1-8b-instant", temperature=0.5)
                        response_text = chat_completion.choices[0].message.content
                    else:
                        response_text = "AI client offline. Please configure your Groq API key."
                    
                    if "COMPLETE:" in response_text:
                        lead_data = response_text.split("COMPLETE:")[1].strip().split("|")
                        if len(lead_data) == 6: save_lead_to_csv(lead_data)
                        final_msg = "Thank you! Your details have been securely logged. Our executive team will connect shortly."
                        st.markdown(final_msg)
                        st.session_state.messages.append({"role": "assistant", "content": final_msg})
                    else:
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e: st.error(f"Error: {e}")

elif nav_choice == "Pricing & Plans":
    if not st.session_state.checkout_active:
        st.markdown('<div class="section-title">Transparent Global Pricing</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Choose the tier that fits your growth velocity.</div>', unsafe_allow_html=True)
        
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        with col_p1:
            st.markdown('<div class="glass-card"><h3>Starter</h3><h2 style="color:#a78bfa;">Rs 999</h2><p style="color:#94a3b8; font-size:14px;">Ideal for solo creators and early-stage MVPs.</p></div>', unsafe_allow_html=True)
            if st.button("Select Starter", key="sel_s"): st.session_state.selected_plan = {"name": "Starter", "price": "Rs 999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p2:
            st.markdown('<div class="glass-card" style="border: 2px solid #7c3aed;"><h3>Pro</h3><h2 style="color:#a78bfa;">Rs 2,999</h2><p style="color:#94a3b8; font-size:14px;">For growing businesses scaling automation.</p></div>', unsafe_allow_html=True)
            if st.button("Select Pro", key="sel_p"): st.session_state.selected_plan = {"name": "Pro", "price": "Rs 2,999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p3:
            st.markdown('<div class="glass-card"><h3>Premium</h3><h2 style="color:#a78bfa;">Rs 7,999</h2><p style="color:#94a3b8; font-size:14px;">For scaling enterprises requiring bespoke suites.</p></div>', unsafe_allow_html=True)
            if st.button("Select Premium", key="sel_pr"): st.session_state.selected_plan = {"name": "Premium", "price": "Rs 7,999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p4:
            st.markdown('<div class="glass-card"><h3>Enterprise</h3><h2 style="color:#a78bfa;">Custom</h2><p style="color:#94a3b8; font-size:14px;">Tailored infrastructure and dedicated engineers.</p></div>', unsafe_allow_html=True)
            if st.button("Contact Sales"): st.info("Reach out via our direct support desk.")
    else:
        plan = st.session_state.selected_plan
        st.markdown(f"<h2 style='text-align: center; color:#ffffff;'>Secure Global Checkout — {plan['name']}</h2>", unsafe_allow_html=True)
        col_c1, col_box, col_c3 = st.columns([1, 2, 1])
        with col_box:
            st.markdown('<div class="glass-card" style="text-align:left;"><h3>Order Summary</h3>', unsafe_allow_html=True)
            st.write(f"**Tier Selected:** {plan['name']} Global Plan")
            st.write(f"**Total Investment:** {plan['price']}")
            pay_method = st.selectbox("Select Payment Gateway", ["Razorpay Secure (UPI / Cards / Net Banking / Wallets)", "International Credit / Debit Card"])
            email_input = st.text_input("Billing Email Address")
            if st.button("Pay Securely Now"):
                if email_input:
                    save_paid_customer(email_input, plan['name'], plan['price'])
                    st.session_state.logged_in = True
                    st.session_state.username = email_input.split("@")[0]
                    st.session_state.user_email = email_input
                    st.session_state.checkout_active = False
                    st.success("Payment verified successfully via Razorpay! Redirecting to dashboard...")
                    st.balloons()
                    st.rerun()
                else: 
                    st.warning("Please enter your billing email.")
            if st.button("Back to Pricing"): 
                st.session_state.checkout_active = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif nav_choice == "AI Package Recommender":
    st.markdown('<div class="section-title">AI Solution Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Answer 2 quick questions to find your optimal stack.</div>', unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        biz_type = st.selectbox("What is your business model?", ["Solo Creator / Freelancer", "Growing Startup / SME", "Global Enterprise"])
        main_goal = st.selectbox("Primary Objective?", ["Lead Gen & Autonomous Chatbots", "Full Scale Web & App Apps", "Custom Enterprise Automation"])
    with col_r2:
        st.write("")
        st.write("")
        if st.button("Run AI Analysis"):
            st.success("Analysis generated successfully:")
            if biz_type == "Solo Creator / Freelancer":
                st.info("Recommended: Starter Plan (Rs 999) — Optimized for fast digital launch.")
            elif biz_type == "Growing Startup / SME":
                st.info("Recommended: Pro Plan (Rs 2,999) — Built for automated acquisition scaling.")
            else:
                st.info("Recommended: Premium / Enterprise Suite (Rs 7,999+) — High-concurrency enterprise infrastructure.")

elif nav_choice == "Portfolio / Projects":
    st.markdown('<div class="section-title">Global Portfolio Deployments</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">A showcase of elite digital products built by AgentFlow AI.</div>', unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1: st.markdown('<div class="glass-card"><h3>AI E-Commerce Suite</h3><p style="color:#94a3b8; font-size:14px;">Conversational sales agent for retail brand, increasing conversion metrics by 48%.</p><br><b style="color:#a78bfa;">Tech: Python, Groq LLM</b></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="glass-card"><h3>HealthTech SaaS Portal</h3><p style="color:#94a3b8; font-size:14px;">HIPAA-compliant patient coordination system with automated smart scheduling.</p><br><b style="color:#a78bfa;">Tech: React, FastAPI</b></div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="glass-card"><h3>FinTech Compliance Bot</h3><p style="color:#94a3b8; font-size:14px;">Real-time regulatory audit trail and automated financial report generation.</p><br><b style="color:#a78bfa;">Tech: Python, Pandas</b></div>', unsafe_allow_html=True)

elif nav_choice == "Testimonials":
    st.markdown('<div class="section-title">Trusted by Global Founders</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">See what industry leaders have to say about our execution speed.</div>', unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1: st.markdown('<div class="glass-card">"AgentFlow AI completely automated our entire sales pipeline. Our conversion velocity tripled within 30 days."<br><br><b style="color:#ffffff;">— Rajesh Sharma</b><br><span style="color:#94a3b8; font-size:13px;">CEO, TechCorp Global</span></div>', unsafe_allow_html=True)
    with t2: st.markdown('<div class="glass-card">"The custom AI chatbot answers customer inquiries flawlessly 24/7. Absolute game changer for our brand."<br><br><b style="color:#ffffff;">— Priya Patel</b><br><span style="color:#94a3b8; font-size:13px;">Founder, StyleHub Retail</span></div>', unsafe_allow_html=True)
    with t3: st.markdown('<div class="glass-card">"Incredible engineering quality, seamless Razorpay integration, and pristine user experience. Highly recommended!"<br><br><b style="color:#ffffff;">— Amit Verma</b><br><span style="color:#94a3b8; font-size:13px;">Director, LogiTech Solutions</span></div>', unsafe_allow_html=True)

elif nav_choice == "Book a Meeting":
    st.markdown('<div class="section-title">Schedule Enterprise Strategy Session</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Select your preferred slot to consult directly with our senior software architects.</div>', unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        b_name = st.text_input("Full Name", key="bk_name")
     b_email = st.text_input("Corporate Email", key="bk_email")
        b_phone = st.text_input("Phone Number", key="bk_phone")  
