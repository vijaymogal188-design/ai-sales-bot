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
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .hero-container { text-align: center; padding: 40px 20px 20px 20px; max-width: 900px; margin: 0 auto; }
    .hero-badge { display: inline-block; background: #ede9fe; color: #7c3aed; font-weight: 700; font-size: 13px; padding: 6px 16px; border-radius: 50px; margin-bottom: 16px; }
    .hero-title { font-size: 42px; font-weight: 800; color: #0f172a; line-height: 1.2; margin-bottom: 16px; }
    .hero-title span { background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero-subtitle { font-size: 16px; color: #64748b; line-height: 1.6; margin-bottom: 25px; }
    .section-title { text-align: center; font-size: 28px; font-weight: 800; color: #0f172a; margin-top: 50px; margin-bottom: 10px; }
    .section-subtitle { text-align: center; font-size: 15px; color: #64748b; margin-bottom: 30px; }
    .pricing-card, .feature-card, .testimonial-card, .portfolio-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 30px; border-radius: 16px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    .checkout-box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 30px; border-radius: 16px; max-width: 600px; margin: 0 auto; }
    .trust-badge-container { display: flex; justify-content: center; gap: 20px; margin: 40px 0; flex-wrap: wrap; }
    .trust-badge { background: #f1f5f9; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 14px; color: #334155; border: 1px solid #cbd5e1; }
    .footer { background: #0f172a; color: #f8fafc; padding: 50px 30px 20px 30px; border-top: 1px solid #1e293b; margin-top: 60px; border-radius: 16px 16px 0 0; }
    .footer a { color: #94a3b8; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Your goal is to converse with the user and collect exactly these 6 details:
1. Name, 2. Business Name, 3. Service Required, 4. Budget, 5. Phone Number, 6. Email Address.
When all 6 are collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "👋 Hello! Welcome to AgentFlow AI. To get started, could you please tell me your name?"})

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_lead_to_csv(data_list):
    file_name = "leads.csv"
    new_lead = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Name": data_list[0].strip(), "Business": data_list[1].strip(), "Service": data_list[2].strip(), "Budget": data_list[3].strip(), "Phone": data_list[4].strip(), "Email": data_list[5].strip()}
    df = pd.DataFrame([new_lead])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def save_paid_customer(email, plan_name, amount):
    file_name = "paid_customers.csv"
    record = {"Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Email": email, "Plan": plan_name, "Amount": amount}
    df = pd.DataFrame([record])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

st.sidebar.markdown("### ⚡ AgentFlow Portal")
st.sidebar.markdown("🟢 **Live Visitors Online:** `142 active`")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio("Navigation", ["Home / Landing Page", "Pricing & Plans", "About Us", "Portfolio / Projects", "Contact Us", "FAQ", "Customer Login / Signup", "Admin Portal", "Legal & Policies"])

st.sidebar.markdown("---")
st.sidebar.markdown("🛡️ **Enterprise Security**")
st.sidebar.caption("SSL Secured | 24/7 Support")

if nav_choice == "Home / Landing Page":
    st.markdown('<div class="hero-container"><div class="hero-badge">⚡ Next-Gen Business Automation & AI</div><div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div><div class="hero-subtitle">Experience lightning-fast client acquisition, intelligent workflow automations, and bespoke digital solutions.</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="trust-badge-container"><div class="trust-badge">🔒 100% Secure Payment</div><div class="trust-badge">🛠️ 24/7 Expert Support</div><div class="trust-badge">🔐 Enterprise SSL Secured</div><div class="trust-badge">⚡ 99.9% Uptime</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Our Professional Services</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1: st.markdown('<div class="feature-card"><h3>🌐 Website</h3><p>Modern responsive sites.</p></div>', unsafe_allow_html=True)
    with col_s2: st.markdown('<div class="feature-card"><h3>🤖 AI Bots</h3><p>24/7 sales bots.</p></div>', unsafe_allow_html=True)
    with col_s3: st.markdown('<div class="feature-card"><h3>📱 Apps</h3><p>iOS & Android apps.</p></div>', unsafe_allow_html=True)
    with col_s4: st.markdown('<div class="feature-card"><h3>🎨 Design</h3><p>Brand identities.</p></div>', unsafe_allow_html=True)
    with col_s5: st.markdown('<div class="feature-card"><h3>📈 Marketing</h3><p>Growth campaigns.</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">💬 Interactive AI Sales Assistant</div>', unsafe_allow_html=True)
    
    col_c1, col_chat, col_c3 = st.columns([1, 2.5, 1])
    with col_chat:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]): st.markdown(message["content"])
        if prompt := st.chat_input("Type your message here..."):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                try:
                    chat_completion = client.chat.completions.create(messages=st.session_state.messages, model="llama-3.1-8b-instant", temperature=0.5)
                    response_text = chat_completion.choices[0].message.content
                    if "COMPLETE:" in response_text:
                        lead_data = response_text.split("COMPLETE:")[1].strip().split("|")
                        if len(lead_data) == 6: save_lead_to_csv(lead_data)
                        final_msg = "Thank you! Your details have been received."
                        st.markdown(final_msg)
                        st.session_state.messages.append({"role": "assistant", "content": final_msg})
                    else:
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e: st.error(f"Error: {e}")

elif nav_choice == "Pricing & Plans":
    if not st.session_state.checkout_active:
        st.markdown('<div class="section-title">Choose Your Growth Plan</div>', unsafe_allow_html=True)
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        with col_p1:
            st.markdown('<div class="pricing-card"><h3>🚀 Starter</h3><h2>₹999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Starter", key="sel_s"): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p2:
            st.markdown('<div class="pricing-card"><h3>💼 Pro</h3><h2>₹2,999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Pro", key="sel_p"): st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p3:
            st.markdown('<div class="pricing-card"><h3>🔥 Premium</h3><h2>₹7,999</h2></div>', unsafe_allow_html=True)
            if st.button("Select Premium", key="sel_pr"): st.session_state.selected_plan = {"name": "Premium", "price": "₹7,999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p4:
            st.markdown('<div class="pricing-card"><h3>🏢 Enterprise</h3><h2>Custom</h2></div>', unsafe_allow_html=True)
            if st.button("Contact Sales"): st.info("Reach out via support desk.")
    else:
        plan = st.session_state.selected_plan
        st.markdown(f"<h2 style='text-align: center;'>🔒 Checkout - {plan['name']}</h2>", unsafe_allow_html=True)
        col_c1, col_box, col_c3 = st.columns([1, 2, 1])
        with col_box:
            st.markdown('<div class="checkout-box"><h3>📋 Order Summary</h3>', unsafe_allow_html=True)
            st.write(f"**Plan:** {plan['name']} | **Price:** {plan['price']}")
            email_input = st.text_input("Billing Email")
            if st.button("Pay & Complete Order"):
                if email_input:
                    save_paid_customer(email_input, plan['name'], plan['price'])
                    st.session_state.logged_in = True; st.session_state.username = email_input.split("@")[0]; st.session_state.checkout_active = False
                    st.success("Payment Successful! Redirecting...")
                    st.balloons(); st.rerun()
                else: st.warning("Enter email.")
            if st.button("⬅️ Back"): st.session_state.checkout_active = False; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            elif nav_choice == "About Us":
    st.markdown('<div class="section-title">About AgentFlow AI</div>', unsafe_allow_html=True)
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("### 🚀 Our Mission")
        st.write("Bridging complex enterprise technology with everyday business efficiency through powerful AI agents.")
    with col_a2:
        st.metric(label="Clients", value="1,200+")
        st.metric(label="Success Rate", value="99.4%")

elif nav_choice == "Portfolio / Projects":
    st.markdown('<div class="section-title">Our Portfolio</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    with p1: st.markdown('<div class="portfolio-card"><h3>🛒 E-Commerce AI</h3><p>Automated sales bot.</p></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="portfolio-card"><h3>🏥 HealthTech SaaS</h3><p>Secure patient portal.</p></div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="portfolio-card"><h3>📊 FinTech Bot</h3><p>Automated reporting.</p></div>', unsafe_allow_html=True)

elif nav_choice == "Contact Us":
    st.markdown('<div class="section-title">Contact Us</div>', unsafe_allow_html=True)
    c_name = st.text_input("Name"); c_email = st.text_input("Email"); c_msg = st.text_area("Message")
    if st.button("Submit Inquiry"):
        if c_name and c_email: st.success("Inquiry sent successfully!")
        else: st.warning("Fill all fields.")

elif nav_choice == "FAQ":
    st.markdown('<div class="section-title">FAQ</div>', unsafe_allow_html=True)
    with st.expander("How does it work?"): st.write("Uses advanced LLMs to interact with users.")
    with st.expander("Is payment secure?"): st.write("Yes, processed securely via Razorpay standards.")

elif nav_choice == "Customer Login / Signup":
    if not st.session_state.logged_in:
        t1, t2 = st.tabs(["Login", "Signup"])
        with t1:
            u = st.text_input("Username", key="l_u"); p = st.text_input("Password", type="password", key="l_p")
            if st.button("Login"):
                if u and p: st.session_state.logged_in = True; st.session_state.username = u; st.success("Success!"); st.rerun()
        with t2:
            nu = st.text_input("Username", key="s_u"); ne = st.text_input("Email", key="s_e"); np = st.text_input("Password", type="password", key="s_p")
            if st.button("Sign Up"):
                if nu and ne: st.session_state.logged_in = True; st.session_state.username = nu; st.success("Created!"); st.rerun()
    else:
        st.markdown(f"## 👋 Welcome, {st.session_state.username}!")
        dt1, dt2, dt3, dt4 = st.tabs(["Status", "Files", "Invoices", "Support"])
        with dt1: st.metric("Project", "AI Sales Agent", "Active")
        with dt2: st.download_button("Download Source Code", "Dummy code", "source.zip")
        with dt3: st.table(pd.DataFrame({"Invoice": ["#INV-1"], "Amount": ["₹999"], "Status": ["Paid"]}))
        with dt4: st.write("Support chat active.")

elif nav_choice == "Admin Portal":
    if not st.session_state.admin_logged_in:
        ap = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            if ap == "admin123": st.session_state.admin_logged_in = True; st.rerun()
            else: st.error("Wrong password!")
    else:
        st.markdown("## 🛡️ Admin Portal")
        at1, at2 = st.tabs(["Paid Customers", "Leads"])
        with at1:
            if os.path.exists("paid_customers.csv"): st.dataframe(pd.read_csv("paid_customers.csv"))
            else: st.warning("No paid customers yet.")
        with at2:
            if os.path.exists("leads.csv"): st.dataframe(pd.read_csv("leads.csv"))
            else: st.warning("No leads yet.")

elif nav_choice == "Legal & Policies":
    st.markdown('<div class="section-title">Legal Policies</div>', unsafe_allow_html=True)
    lt1, lt2, lt3 = st.tabs(["Privacy", "Terms", "Refund"])
    with lt1: st.write("Privacy policy details here.")
    with lt2: st.write("Terms & conditions here.")
    with lt3: st.write("Refund policy details here.")
