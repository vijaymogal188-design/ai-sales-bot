import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS Portal", 
    page_icon="⚡", 
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
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
        margin-top: 40px;
        margin-bottom: 10px;
    }
    .section-subtitle {
        text-align: center;
        font-size: 15px;
        color: #64748b;
        margin-bottom: 30px;
    }
    .pricing-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .footer {
        text-align: center;
        padding: 30px;
        color: #94a3b8;
        font-size: 14px;
        border-top: 1px solid #e2e8f0;
        margin-top: 50px;
        background: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq Client securely
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
nav_choice = st.sidebar.radio("Navigation", ["Home / Landing Page", "Pricing & Plans", "Customer Login / Signup", "Admin Portal"])

if nav_choice == "Home / Landing Page":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">⚡ Next-Gen Business Automation</div>
            <div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div>
            <div class="hero-subtitle">Experience lightning-fast client acquisition, intelligent workflow automations, and bespoke digital solutions designed to elevate your brand.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Our Professional Services</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Comprehensive solutions tailored to scale your digital presence.</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1:
        st.markdown("### 🌐 Website Dev")
        st.write("High-performing modern responsive websites.")
    with col_s2:
        st.markdown("### 🤖 AI Chatbots")
        st.write("24/7 intelligent sales conversational bots.")
    with col_s3:
        st.markdown("### 📱 App Dev")
        st.write("Scalable mobile apps for iOS & Android.")
    with col_s4:
        st.markdown("### 🎨 Logo Design")
        st.write("Memorable brand identities & graphics.")
    with col_s5:
        st.markdown("### 📈 Marketing")
        st.write("Data-driven customer growth campaigns.")

    st.markdown("---")

    st.markdown('<div class="section-title">💬 Interactive AI Sales Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Chat with our assistant below to share your custom requirements.</div>', unsafe_allow_html=True)

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
            <p>© 2026 <span>AgentFlow AI</span>. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

elif nav_choice == "Pricing & Plans":
    st.markdown('<div class="section-title">Choose Your Growth Plan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Secure checkout via Razorpay with automatic account creation and instant login access.</div>', unsafe_allow_html=True)

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)

    with col_p1:
        st.markdown("""
            <div class="pricing-card">
                <h3>🚀 Starter</h3>
                <h2>₹999</h2>
                <p>Ideal for solo creators and small projects.</p>
            </div>
        """, unsafe_allow_html=True)
        email_1 = st.text_input("Enter your Email", key="email_starter")
        if st.button("Pay ₹999 with Razorpay", key="btn_starter"):
            if email_1:
                save_paid_customer(email_1, "Starter", "₹999")
                st.session_state.logged_in = True
                st.session_state.username = email_1.split("@")[0]
                st.success("Payment Successful via Razorpay! Account created automatically.")
                st.info(f"📩 Login credentials & receipt sent to {email_1}")
                st.balloons()
            else:
                st.warning("Please enter your email address.")

    with col_p2:
        st.markdown("""
            <div class="pricing-card" style="border: 2px solid #7c3aed;">
                <h3>💼 Pro</h3>
                <h2>₹2,999</h2>
                <p>Great for growing businesses looking for automation.</p>
            </div>
        """, unsafe_allow_html=True)
        email_2 = st.text_input("Enter your Email", key="email_pro")
        if st.button("Pay ₹2,999 with Razorpay", key="btn_pro"):
            if email_2:
                save_paid_customer(email_2, "Pro", "₹2,999")
                st.session_state.logged_in = True
                st.session_state.username = email_2.split("@")[0]
                st.success("Payment Successful via Razorpay! Account created automatically.")
                st.info(f"📩 Login credentials & receipt sent to {email_2}")
                st.balloons()
            else:
                st.warning("Please enter your email address.")

    with col_p3:
        st.markdown("""
            <div class="pricing-card">
                <h3>🔥 Premium</h3>
                <h2>₹7,999</h2>
                <p>Advanced capabilities for scaling agencies & enterprises.</p>
            </div>
        """, unsafe_allow_html=True)
        email_3 = st.text_input("Enter your Email", key="email_premium")
        if st.button("Pay ₹7,999 with Razorpay", key="btn_premium"):
            if email_3:
                save_paid_customer(email_3, "Premium", "₹7,999")
                st.session_state.logged_in = True
                st.session_state.username = email_3.split("@")[0]
                st.success("Payment Successful via Razorpay! Account created automatically.")
                st.info(f"📩 Login credentials & receipt sent to {email_3}")
                st.balloons()
            else:
                st.warning("Please enter your email address.")

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

elif nav_choice == "Customer Login / Signup":
    if not st.session_state.logged_in:
        st.markdown("<h2 style='text-align: center;'>🔐 Customer Portal Authentication</h2>", unsafe_allow_html=True)
        
        auth_tab1, auth_tab2 = st.tabs(["🔑 Login", "📝 Signup"])
        
        with auth_tab1:
            st.subheader("Login to your Dashboard")
            login_user = st.text_input("Username or Email", key="login_email")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login"):
                if login_user and login_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.success("Login successful! Redirecting to Dashboard...")
                    st.rerun()
                else:
                    st.warning("Please fill in both fields.")
                    
        with auth_tab2:
            st.subheader("Create a New Account")
            new_user = st.text_input("Choose a Username", key="signup_user")
            new_email = st.text_input("Email Address", key="signup_email")
            new_pass = st.text_input("Create Password", type="password", key="signup_pass")
            
            if st.button("Sign Up"):
                if new_user and new_email and new_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = new_user
                    st.success("Account created successfully! Welcome.")
                    st.rerun()
                else:
                    st.warning("Please fill in all details.")

    else:
        st.markdown(f"## 👋 Welcome back, {st.session_state.username}!")
        st.info("Here is your centralized project control room and client workspace.")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

        dash_tab1, dash_tab2, dash_tab3, dash_tab4 = st.tabs([
            "📊 Project Status", 
            "📁 My Projects & Files", 
            "💳 Invoices", 
            "💬 Chat with Support"
        ])
        
        with dash_tab1:
            st.subheader("Active Project Tracking")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Current Project", value="AI Sales Agent MVP", delta="Phase 2")
            with col2:
                st.metric(label="Status", value="In Progress 🔄", delta="On Track")
            with col3:
                st.metric(label="Estimated Delivery", value="5 Days Left")
            
            st.write("---")
            st.write("### Milestone Timeline")
            st.progress(70, text="70% Project Completion Completed")
            st.markdown("- ✅ **Milestone 1:** Architecture & Requirements Setup")
            st.markdown("- ✅ **Milestone 2:** Groq AI Model Integration & Prompt Design")
            st.markdown("- 🔄 **Milestone 3:** SaaS Landing Page & UI Polish (In Progress)")
            st.markdown("- ⏳ **Milestone 4:** Final QA Testing & Live Deployment")

        with dash_tab2:
            st.subheader("📦 My Projects & Deliverables")
            st.write("Download your project source codes, reports, and assets below:")
            
            st.download_button(
                label="📥 Download Project Source Code (.zip)",
                data="Dummy project source code bytes data",
                file_name="agentflow_project_files.zip",
                mime="application/zip"
            )
            
            st.markdown("---")
            st.subheader("Project History")
            project_data = {
                "Project ID": ["#PRJ-101", "#PRJ-102"],
                "Service Name": ["AI Chatbot Implementation", "Website Development"],
                "Status": ["Completed ✅", "In Progress 🔄"],
                "Date Started": ["2026-01-15", "2026-02-01"]
            }
            st.table(pd.DataFrame(project_data))

        with dash_tab3:
            st.subheader("💳 Billing & Invoices")
            invoice_data = {
                "Invoice ID": ["#INV-2026-01", "#INV-2026-02"],
                "Description": ["Starter Tier Setup", "Monthly Maintenance"],
                "Amount": ["₹999", "₹2,999"],
                "Status": ["Paid 🟢", "Pending 🟡"]
            }
            st.table(pd.DataFrame(invoice_data))
            
            if st.button("Download Latest Invoice PDF"):
                st.success("Invoice #INV-2026-02 downloaded successfully!")

        with dash_tab4:
            st.subheader("💬 Direct Support Desk")
            st.write("Have a question about your build? Chat directly with our technical support engineer.")
            
            if "support_msgs" not in st.session_state:
                st.session_state.support_msgs = [{"role": "assistant", "content": "Hello! How can our support team assist you with your project today?"}]
                
            for msg in st.session_state.support_msgs:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    
            if sup_prompt := st.chat_input("Ask support a question..."):
                st.session_state.support_msgs.append({"role": "user", "content": sup_prompt})
                with st.chat_message("user"):
                    st.markdown(sup_prompt)
                    
                reply = "Thank you for reaching out! A human support expert has received your query and will respond via email shortly."
                st.session_state.support_msgs.append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.markdown(reply)

elif nav_choice == "Admin Portal":
    if not st.session_state.admin_logged_in:
        st.markdown("<h2 style='text-align: center;'>🔒 Admin Authentication</h2>", unsafe_allow_html=True)
        
        col_ad1, col_ad2, col_ad3 = st.columns([1, 2, 1])
        with col_ad2:
            admin_pass = st.text_input("Enter Admin Secret Password", type="password")
            if st.button("Login as Admin"):
                if admin_pass == "admin123":
                    st.session_state.admin_logged_in = True
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect password! Try 'admin123'")
    else:
        st.markdown("## 🛡️ Admin Portal - Notifications & Leads")
        
        if st.sidebar.button("Admin Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        admin_tab1, admin_tab2 = st.tabs(["🔔 Paid Customers (Notifications)", "📋 Captured AI Leads"])
        
        with admin_tab1:
            st.subheader("Notifications of New Paid Customers")
            if os.path.exists("paid_customers.csv"):
                df_paid = pd.read_csv("paid_customers.csv")
                if not df_paid.empty:
                    st.success(f"🔔 You have {len(df_paid)} new paid customer(s) registered!")
                    st.dataframe(df_paid, use_container_width=True)
                    
                    csv_paid = df_paid.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Paid Customers CSV",
                        data=csv_paid,
                        file_name=f"paid_customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No paid customers yet.")
            else:
                st.warning("No paid customers records found yet.")
                
        with admin_tab2:
            st.subheader("Captured Leads from AI Sales Bot")
            if os.path.exists("leads.csv"):
                df_leads = pd.read_csv("leads.csv")
                if not df_leads.empty:
                    search_query = st.text_input("🔍 Search Leads (by Name, Email, Business, or Service):")
                    if search_query:
                        mask = df_leads.apply(lambda row: row.astype(str).str.contains(search_qu
