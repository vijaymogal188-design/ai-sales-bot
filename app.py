import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise SaaS & Business Automation", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
        color: #0f172a;
    }

    .stApp {
        background-color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    .hero-container {
        text-align: center;
        padding: 50px 20px 30px 20px;
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
        font-size: 46px;
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
        margin-bottom: 30px;
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
        transition: transform 0.3s ease;
    }
    .pricing-card:hover, .feature-card:hover, .testimonial-card:hover, .portfolio-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.1);
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
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. Your goal is to converse with the user and collect exactly these 6 details:
1. Name, 2. Business Name, 3. Service Required, 4. Budget, 5. Phone Number, 6. Email Address.
When all 6 are collected, output EXACTLY: COMPLETE: Name | Business | Service | Budget | Phone | Email"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "👋 Hello! Welcome to AgentFlow AI. To get started, could you please tell me your name?"
    })

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "admin_logged_in" not in st.session_state: st.session_state.admin_logged_in = False
if "selected_plan" not in st.session_state: st.session_state.selected_plan = None
if "checkout_active" not in st.session_state: st.session_state.checkout_active = False

def save_user_to_csv(username, email, password):
    file_name = "users.csv"
    new_user = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Username": username,
        "Email": email,
        "Password": password
    }
    df = pd.DataFrame([new_user])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def save_lead_to_csv(data_list):
    file_name = "leads.csv"
    new_lead = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": data_list[0].strip(),
        "Business": data_list[1].strip(),
        "Service": data_list[2].strip(),
        "Budget": data_list[3].strip(),
        "Phone": data_list[4].strip(),
        "Email": data_list[5].strip(),
        "Status": "New",
        "Notes": "None"
    }
    df = pd.DataFrame([new_lead])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def save_paid_customer(email, plan_name, amount):
    file_name = "paid_customers.csv"
    record = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Email": email,
        "Plan": plan_name,
        "Amount": amount,
        "Project Status": "In Progress",
        "Notes": "New subscription paid"
    }
    df = pd.DataFrame([record])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def save_booking_to_csv(name, email, phone, service, date, time_slot):
    file_name = "bookings.csv"
    record = {
        "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Customer Name": name,
        "Email": email,
        "Phone": phone,
        "Service": service,
        "Meeting Date": str(date),
        "Time Slot": str(time_slot),
        "Status": "Pending",
        "Notes": "Scheduled consultation"
    }
    df = pd.DataFrame([record])
    if not os.path.exists(file_name): df.to_csv(file_name, index=False)
    else: df.to_csv(file_name, mode='a', header=False, index=False)

def generate_invoice_pdf(email, plan, amount):
    return f"""
    AGENTFLOW AI - OFFICIAL INVOICE
    -----------------------------------
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Customer Email: {email}
    Plan Selected: {plan}
    Payment Methods: Razorpay (UPI / Cards / Net Banking / Wallet)
    Amount Paid: {amount}
    Status: SUCCESSFUL / VERIFIED
    -----------------------------------
    Thank you for your business!
    """

st.sidebar.markdown("### ⚡ AgentFlow AI")
st.sidebar.caption("Enterprise SaaS Portal v3.2")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio("Navigation", [
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

st.sidebar.markdown("---")
st.sidebar.markdown("🛡️ **Enterprise Security**")
st.sidebar.caption("SSL Secured | 24/7 Support")

if nav_choice == "Home / Landing Page":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">⚡ Next-Gen Business Automation & AI</div>
            <div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div>
            <div class="hero-subtitle">Experience lightning-fast client acquisition, intelligent workflow automations, and bespoke digital solutions designed to elevate your brand globally.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Our Professional Services</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    with col_s1: st.markdown('<div class="feature-card"><h3>🌐 Website Dev</h3><p>Modern responsive sites.</p></div>', unsafe_allow_html=True)
    with col_s2: st.markdown('<div class="feature-card"><h3>🤖 AI Chatbots</h3><p>24/7 intelligent sales bots.</p></div>', unsafe_allow_html=True)
    with col_s3: st.markdown('<div class="feature-card"><h3>📱 App Dev</h3><p>Scalable mobile apps.</p></div>', unsafe_allow_html=True)
    with col_s4: st.markdown('<div class="feature-card"><h3>🎨 Logo Design</h3><p>Memorable brand identities.</p></div>', unsafe_allow_html=True)
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
                        final_msg = "Thank you! Your details have been received. Our team will contact you soon."
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
            st.markdown('<div class="pricing-card"><h3>🚀 Starter</h3><h2>₹999</h2><p>Ideal for solo creators.</p></div>', unsafe_allow_html=True)
            if st.button("Select Starter", key="sel_s"): st.session_state.selected_plan = {"name": "Starter", "price": "₹999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p2:
            st.markdown('<div class="pricing-card" style="border: 2px solid #7c3aed;"><h3>💼 Pro</h3><h2>₹2,999</h2><p>For growing businesses.</p></div>', unsafe_allow_html=True)
            if st.button("Select Pro", key="sel_p"): st.session_state.selected_plan = {"name": "Pro", "price": "₹2,999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p3:
            st.markdown('<div class="pricing-card"><h3>🔥 Premium</h3><h2>₹7,999</h2><p>For scaling enterprises.</p></div>', unsafe_allow_html=True)
            if st.button("Select Premium", key="sel_pr"): st.session_state.selected_plan = {"name": "Premium", "price": "₹7,999"}; st.session_state.checkout_active = True; st.rerun()
        with col_p4:
            st.markdown('<div class="pricing-card"><h3>🏢 Enterprise</h3><h2>Custom</h2><p>Tailored solutions.</p></div>', unsafe_allow_html=True)
            if st.button("Contact Sales"): st.info("Reach out via support desk.")
    else:
        plan = st.session_state.selected_plan
        st.markdown(f"<h2 style='text-align: center;'>🔒 Secure Checkout - {plan['name']}</h2>", unsafe_allow_html=True)
        col_c1, col_box, col_c3 = st.columns([1, 2, 1])
        with col_box:
            st.markdown('<div class="checkout-box" style="background:#ffffff; padding:30px; border-radius:16px; border:1px solid #e2e8f0;"><h3>📋 Order Summary</h3>', unsafe_allow_html=True)
            st.write(f"**Plan Tier:** {plan['name']} Subscription")
            st.write(f"**Total Amount:** {plan['price']}")
            pay_method = st.selectbox("Select Payment Method", ["Razorpay (UPI / Google Pay / PhonePe / Paytm)", "Credit / Debit Cards", "Net Banking", "Mobile Wallets"])
            email_input = st.text_input("Billing Email Address")
            if st.button("Pay Securely with Razorpay"):
                if email_input:
                    save_paid_customer(email_input, plan['name'], plan['price'])
                    st.session_state.logged_in = True
                    st.session_state.username = email_input.split("@")[0]
                    st.session_state.user_email = email_input
                    st.session_state.checkout_active = False
                    st.success("Payment Successful via Razorpay! Redirecting to Dashboard...")
                    st.balloons()
                    st.rerun()
                else: 
                    st.warning("Please enter your email.")
            if st.button("⬅️ Back to Pricing"): 
                st.session_state.checkout_active = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif nav_choice == "AI Package Recommender":
    st.markdown('<div class="section-title">🤖 AI Package Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Answer 2 quick questions and let our AI suggest the best plan for you!</div>', unsafe_allow_html=True)
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        biz_type = st.selectbox("What is your business type?", ["Solo Creator / Freelancer", "Growing Startup / SME", "Large Enterprise"])
        main_goal = st.selectbox("What is your primary goal?", ["Lead Generation & Chatbots", "Full Website & App Development", "Custom Enterprise Automation"])
    with col_r2:
        st.write("")
        st.write("")
        if st.button("✨ Get AI Recommendation"):
            st.success("Analysis complete! Based on your profile:")
            if biz_type == "Solo Creator / Freelancer":
                st.info("🚀 **Recommended Plan: Starter (₹999)** - Perfect for getting your digital presence off the ground.")
            elif biz_type == "Growing Startup / SME":
                st.info("💼 **Recommended Plan: Pro (₹2,999)** - Ideal for scaling automated customer acquisition.")
            else:
                st.info("🔥 **Recommended Plan: Premium / Enterprise (₹7,999+)** - Built for heavy enterprise automation.")

elif nav_choice == "Portfolio / Projects":
    st.markdown('<div class="section-title">Our Portfolio & Project Cards</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Explore our previous successful client deployments.</div>', unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1: st.markdown('<div class="portfolio-card"><h3>🛒 AI E-Commerce Suite</h3><p>Automated conversational sales bot for retail brand, boosting conversion by 45%.</p><br><b>Tech:</b> Python, Groq AI</div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="portfolio-card"><h3>🏥 HealthTech SaaS</h3><p>Secure patient management portal with automated billing and scheduling.</p><br><b>Tech:</b> React, FastAPI</div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="portfolio-card"><h3>📊 FinTech Analytics Bot</h3><p>Real-time financial compliance and automated tax report generation.</p><br><b>Tech:</b> Python, Pandas</div>', unsafe_allow_html=True)

elif nav_choice == "Testimonials":
    st.markdown('<div class="section-title">⭐ Client Testimonials</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Hear what founders and industry leaders say about AgentFlow AI.</div>', unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1: st.markdown('<div class="testimonial-card">"AgentFlow AI automated our entire lead pipeline. Conversion rate jumped by 300%!"<br><br><b>— Rajesh Sharma</b><br><span style="color:#64748b;">CEO, TechCorp</span></div>', unsafe_allow_html=True)
    with t2: st.markdown('<div class="testimonial-card">"The custom AI chatbot handles customer queries 24/7 flawlessly. Exceptional work!"<br><br><b>— Priya Patel</b><br><span style="color:#64748b;">Founder, StyleHub</span></div>', unsafe_allow_html=True)
    with t3: st.markdown('<div class="testimonial-card">"Incredible platform and seamless Razorpay payment integration. Highly recommended!"<br><br><b>— Amit Verma</b><br><span style="color:#64748b;">Director, LogiTech</span></div>', unsafe_allow_html=True)

elif nav_choice == "Book a Meeting":
    st.markdown('<div class="section-title">📅 Enterprise Meeting Booking System</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Select your preferred date, time slot, and service to schedule a strategy consultation.</div>', unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        b_name = st.text_input("Full Name", key="bk_name")
        b_email = st.text_input("Email Address", key="bk_email")
        b_phone = st.text_input("Phone Number", key="bk_phone")
    with col_b2:
        b_service = st.selectbox("Service Required", ["AI Chatbot Implementation", "Website Development", "Mobile App Development", "Enterprise Automation", "General Consultation"])
        b_date = st.date_input("Select Meeting Date", key="bk_date")
        b_time = st.selectbox("Select Time Slot", ["10:00 AM - 11:00 AM", "11:30 AM - 12:30 PM", "02:00 PM - 03:00 PM", "04:00 PM - 05:00 PM"])

    st.write("")
    if st.button("Submit Meeting Booking"):
        if b_name and b_email and b_phone:
            save_booking_to_csv(b_name, b_email, b_phone, b_service, b_date, b_time)
            st.success(f"🎉 Booking successfully submitted for {b_date} ({b_time})! Your appointment status is currently **Pending**. Our team will confirm shortly.")
            st.balloons()
        else:
            st.warning("Please fill in your Name, Email, and Phone Number.")

elif nav_choice == "Contact Us":
    st.markdown('<div class="section-title">Contact Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Inquiries submitted here are directly routed to the Admin CRM Dashboard.</div>', unsafe_allow_html=True)
    
    c_name = st.text_input("Your Full Name")
    c_email = st.text_input("Your Email Address")
    c_service = st.selectbox("Service Interested In", ["Website Dev", "AI Chatbot", "App Dev", "Logo Design", "Marketing"])
    c_msg = st.text_area("Your Message")
    
    if st.button("Submit Inquiry"):
        if c_name and c_email and c_msg:
            save_lead_to_csv([c_name, "Inquiry Form", c_service, "Custom", "N/A", c_email])
            st.success("✅ Inquiry successfully submitted! Our team and CRM dashboard have received your message.")
        else:
            st.warning("Please fill in all required fields.")

elif nav_choice == "Admin CRM Dashboard":
    if not st.session_state.admin_logged_in:
        st.markdown("<h2 style='text-align: center;'>🔒 Admin Authentication</h2>", unsafe_allow_html=True)
        col_ad1, col_ad2, col_ad3 = st.columns([1, 2, 1])
        with col_ad2:
            admin_pass = st.text_input("Enter Admin Password", type="password", key="admin_pass_input_field")
            if st.button("Login as Admin", key="admin_login_action_btn"):
                if admin_pass == "admin123": 
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else: 
                    st.error("Incorrect password! Try 'admin123'")
    else:
        st.markdown("## 🛡️ Enterprise Admin CRM & Analytics Dashboard")
        if st.sidebar.button("Admin Logout", key="admin_sidebar_logout_btn"): 
            st.session_state.admin_logged_in = False
            st.rerun()

        # Safe CSV loading with try/except
        try:
            users_df = pd.read_csv("users.csv") if os.path.exists("users.csv") else pd.DataFrame(columns=["Date", "Username", "Email", "Password"])
        except Exception:
            users_df = pd.DataFrame(columns=["Date", "Username", "Email", "Password"])

        try:
            leads_df = pd.read_csv("leads.csv") if os.path.exists("leads.csv") else pd.DataFrame(columns=["Date", "Name", "Business", "Service", "Budget", "Phone", "Email", "Status", "Notes"])
        except Exception:
            leads_df = pd.DataFrame(columns=["Date", "Name", "Business", "Service", "Budget", "Phone", "Email", "Status", "Notes"])

        try:
            bookings_df = pd.read_csv("bookings.csv") if os.path.exists("bookings.csv") else pd.DataFrame(columns=["Submission Date", "Customer Name", "Email", "Phone", "Service", "Meeting Date", "Time Slot", "Status", "Notes"])
        except Exception:
            bookings_df = pd.DataFrame(columns=["Submission Date", "Customer Name", "Email", "Phone", "Service", "Meeting Date", "Time Slot", "Status", "Notes"])

        try:
            customers_df = pd.read_csv("paid_customers.csv") if os.path.exists("paid_customers.csv") else pd.DataFrame(columns=["Date", "Email", "Plan", "Amount", "Project Status", "Notes"])
        except Exception:
            customers_df = pd.DataFrame(columns=["Date", "Email", "Plan", "Amount", "Project Status", "Notes"])

        total_users = len(users_df) if not users_df.empty else 0
        total_leads = len(leads_df) if not leads_df.empty else 0
        total_bookings = len(bookings_df) if not bookings_df.empty else 0
        paid_customers = len(customers_df) if not customers_df.empty else 0
        
        total_revenue = 0
        if not customers_df.empty and "Amount" in customers_df.columns:
            for amt in customers_df["Amount"]:
                clean_amt = str(amt).replace("₹", "").replace(",", "").strip()
                if clean_amt.isdigit():
                    total_revenue += int(clean_amt)

        active_projects = 0
        if not customers_df.empty and "Project Status" in customers_df.columns:
            active_projects = len(customers_df[customers_df["Project Status"] == "In Progress"])

        st.markdown("### 📊 Overview Metrics")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1: st.metric(label="👥 Total Users", value=total_users)
        with m2: st.metric(label="📋 Total Leads", value=total_leads)
        with m3: st.metric(label="📅 Total Bookings", value=total_bookings)
        with m4: st.metric(label="💳 Paid Customers", value=paid_customers)
        with m5: st.metric(label="💰 Total Revenue", value=f"₹{total_revenue:,}")
        with m6: st.metric(label="⚙️ Active Projects", value=active_projects)

        st.markdown("---")

        st.markdown("### 🔍 Global Search Across CRM Data")
        global_query = st.text_input("Type to search across Users, Leads, Bookings, and Customers...", key="admin_global_search_input")
        if global_query:
            st.info(f"Showing global search results matching: '{global_query}'")
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                st.subheader("Users Match")
                if not users_df.empty:
                    u_match = users_df[users_df.astype(str).apply(lambda x: x.str.contains(global_query, case=False)).any(axis=1)]
                    if not u_match.empty:
                        st.dataframe(u_match, use_container_width=True)
                    else:
                        st.info("No matching users found.")
                else:
                    st.info("No data available.")

                st.subheader("Leads Match")
                if not leads_df.empty:
                    l_match = leads_df[leads_df.astype(str).apply(lambda x: x.str.contains(global_query, case=False)).any(axis=1)]
                    if not l_match.empty:
                        st.dataframe(l_match, use_container_width=True)
                    else:
                        st.info("No matching leads found.")
                else:
                    st.info("No data available.")

            with g_col2:
                st.subheader("Bookings Match")
                if not bookings_df.empty:
                    b_match = bookings_df[bookings_df.astype(str).apply(lambda x: x.str.contains(global_query, case=False)).any(axis=1)]
                    if not b_match.empty:
                        st.dataframe(b_match, use_container_width=True)
                    else:
                        st.info("No matching bookings found.")
                else:
                    st.info("No data available.")

                st.subheader("Customers Match")
                if not customers_df.empty:
                    c_match = customers_df[customers_df.astype(str).apply(lambda x: x.str.contains(global_query, case=False)).any(axis=1)]
                    if not c_match.empty:
                        st.dataframe(c_match, use_container_width=True)
                    else:
                        st.info("No matching customers found.")
                else:
                    st.info("No data available.")
            st.markdown("---")

        crm_tab1, crm_tab2, crm_tab3, crm_tab4, crm_tab5 = st.tabs([
            "👥 Users Management", 
            "📋 Leads Management", 
            "📅 Bookings Management", 
            "💼 Paid Customers", 
            "📈 Analytics & Growth"
        ])

        with crm_tab1:
            st.subheader("Registered Users Directory")
            if not users_df.empty:
                u_search = st.text_input("🔍 Search Users by Username or Email", key="admin_user_search_box")
                filtered_users = users_df.copy()
                if u_search:
                    mask = filtered_users.astype(str).apply(lambda x: x.str.contains(u_search, case=False)).any(axis=1)
                    filtered_users = filtered_users[mask]

                st.dataframe(filtered_users, use_container_width=True)
                st.download_button("📥 Export Users CSV", data=filtered_users.to_csv(index=False).encode('utf-8'), file_name="users_export.csv", mime="text/csv", key="admin_exp_users_btn")

                st.markdown("#### Edit or Delete User")
                u_idx = st.number_input("Select Row Index to Edit/Delete", min_value=0, max_value=max(0, len(users_df)-1), step=1, key="admin_user_idx_input")
                if len(users_df) > 0:
                    selected_user = users_df.iloc[u_idx]
                    with st.form("edit_user_form_admin"):
                        new_u_name = st.text_input("Username", value=str(selected_user["Username"]))
                        new_u_email = st.text_input("Email", value=str(selected_user["Email"]))
                        new_u_pass = st.text_input("Password", value=str(selected_user["Password"]))
                        col_u1, col_u2 = st.columns(2)
                        update_user_btn = col_u1.form_submit_button("💾 Save Changes")
                        delete_user_btn = col_u2.form_submit_button("🗑️ Delete User")

                        if update_user_btn:
                            users_df.at[u_idx, "Username"] = new_u_name
                            users_df.at[u_idx, "Email"] = new_u_email
                            users_df.at[u_idx, "Password"] = new_u_pass
                            users_df.to_csv("users.csv", index=False)
                            st.success("User updated successfully!")
                            st.rerun()

                        if delete_user_btn:
                            users_df = users_df.drop(u_idx).reset_index(drop=True)
                            users_df.to_csv("users.csv", index=False)
                            st.success("User deleted successfully!")
                            st.rerun()
            else:
                st.info("No data available.")

        with crm_tab2:
            st.subheader("Sales Leads & Inquiries CRM")
            if not leads_df.empty:
                col_l1, col_l2 = st.columns(2)
                with col_l1:
                    l_search = st.text_input("🔍 Search Leads by Name/Email/Service", key="admin_lead_search_box")
                with col_l2:
                    lead_statuses = ["All"] + list(leads_df["Status"].unique()) if "Status" in leads_df.columns and not leads_df["Status"].isnull().all() else ["All"]
                    l_status_filter = st.selectbox("Filter by Status", lead_statuses, key="admin_lead_status_selectbox")

                filtered_leads = leads_df.copy()
                if l_search:
                    mask = filtered_leads.astype(str).apply(lambda x: x.str.contains(l_search, case=False)).any(axis=1)
                    filtered_leads = filtered_leads[mask]
                if l_status_filter != "All" and "Status" in filtered_leads.columns:
                    filtered_leads = filtered_leads[filtered_leads["Status"] == l_status_filter]

                st.dataframe(filtered_leads, use_container_width=True)
                st.download_button("📥 Export Filtered Leads CSV", data=filtered_leads.to_csv(index=False).encode('utf-8'), file_name="leads_export.csv", mime="text/csv", key="admin_exp_leads_btn")

                st.markdown("#### Update Lead Status or Delete")
                l_idx = st.number_input("Select Lead Row Index", min_value=0, max_value=max(0, len(leads_df)-1), step=1, key="admin_lead_idx_input")
                if len(leads_df) > 0:
                    selected_lead = leads_df.iloc[l_idx]
                    with st.form("edit_lead_form_admin"):
                        current_status = str(selected_lead["Status"]) if "Status" in selected_lead and pd.notna(selected_lead["Status"]) else "New"
                        status_options = ["New", "Contacted", "Converted", "Closed"]
                        default_idx = status_options.index(current_status) if current_status in status_options else 0
                        new_status = st.selectbox("Update Status", status_options, index=default_idx)
                        col_le1, col_le2 = st.columns(2)
                        update_lead_btn = col_le1.form_submit_button("💾 Update Status")
                        delete_lead_btn = col_le2.form_submit_button("🗑️ Delete Lead")

                        if update_lead_btn:
                            leads_df.at[l_idx, "Status"] = new_status
                            leads_df.to_csv("leads.csv", index=False)
                            st.success("Lead status updated!")
                            st.rerun()

                        if delete_lead_btn:
                            leads_df = leads_df.drop(l_idx).reset_index(drop=True)
                            leads_df.to_csv("leads.csv", index=False)
                            st.success("Lead deleted successfully!")
                            st.rerun()
            else:
                st.info("No data available.")

        with crm_tab3:
            st.subheader("Consultation Bookings Management")
            if not bookings_df.empty:
                b_search = st.text_input("🔍 Search Bookings by Client Name or Email", key="admin_booking_search_box")
                filtered_bookings = bookings_df.copy()
                if b_search:
                    mask = filtered_bookings.astype(str).apply(lambda x: x.str.contains(b_search, case=False)).any(axis=1)
                    filtered_bookings = filtered_bookings[mask]

                st.dataframe(filtered_bookings, use_container_width=True)
                st.download_button("📥 Export Bookings CSV", data=filtered_bookings.to_csv(index=False).encode('utf-8'), file_name="bookings_export.csv", mime="text/csv", key="admin_exp_bookings_btn")

                st.markdown("#### Confirm, Cancel, or Delete Booking")
                b_idx = st.number_input("Select Booking Row Index", min_value=0, max_value=max(0, len(bookings_df)-1), step=1, key="admin_booking_idx_input")
                if len(bookings_df) > 0:
                    col_b1, col_b2, col_b3 = st.columns(3)
                    if col_b1.button("✅ Confirm Booking", key="admin_conf_book_btn"):
                        bookings_df.at[b_idx, "Status"] = "Confirmed"
                        bookings_df.to_csv("bookings.csv", index=False)
                        st.success("Booking Confirmed!")
                        st.rerun()
                    if col_b2.button("❌ Cancel Booking", key="admin_canc_book_btn"):
                        bookings_df.at[b_idx, "Status"] = "Cancelled"
                        bookings_df.to_csv("bookings.csv", index=False)
                        st.warning("Booking Cancelled.")
                        st.rerun()
                    if col_b3.button("🗑️ Delete Booking Record", key="admin_del_book_btn"):
                        bookings_df = bookings_df.drop(b_idx).reset_index(drop=True)
                        bookings_df.to_csv("bookings.csv", index=False)
                        st.success("Booking deleted.")
                        st.rerun()
            else:
                st.info("No data available.")

        with crm_tab4:
            st.subheader("Paid Subscriptions & Project Status")
            if not customers_df.empty:
                c_search = st.text_input("🔍 Search Customers by Email or Plan", key="admin_customer_search_box")
                filtered_customers = customers_df.copy()
                if c_search:
                    mask = filtered_customers.astype(str).apply(lambda x: x.str.contains(c_search, case=False)).any(axis=1)
                    filtered_customers = filtered_customers[mask]

                st.dataframe(filtered_customers, use_container_width=True)
                st.download_button("📥 Export Customers CSV", data=filtered_customers.to_csv(index=False).encode('utf-8'), file_name="customers_export.csv", mime="text/csv", key="admin_exp_cust_btn")

                st.markdown("#### Update Project Status, Download Invoice, or Delete")
                c_idx = st.number_input("Select Customer Row Index", min_value=0, max_value=max(0, len(customers_df)-1), step=1, key="admin_customer_idx_input")
                if len(customers_df) > 0:
                    sel_cust = customers_df.iloc[c_idx]
                    with st.form("edit_customer_form_admin"):
                        curr_proj_status = str(sel_cust["Project Status"]) if "Project Status" in sel_cust and pd.notna(sel_cust["Project Status"]) else "In Progress"
                        proj_statuses = ["In Progress", "Review", "Completed", "On Hold"]
                        default_p_idx = proj_statuses.index(curr_proj_status) if curr_proj_status in proj_statuses else 0
                        new_proj_status = st.selectbox("Project Status", proj_statuses, index=default_p_idx)
                        
                        col_ce1, col_ce2 = st.columns(2)
                        update_cust_btn = col_ce1.form_submit_button("💾 Update Project Status")
                        delete_cust_btn = col_ce2.form_submit_button("🗑️ Delete Customer Record")

                        if update_cust_btn:
                            customers_df.at[c_idx, "Project Status"] = new_proj_status
                            customers_df.to_csv("paid_customers.csv", index=False)
                            st.success("Project status updated successfully!")
                            st.rerun()

                        if delete_cust_btn:
                            customers_df = customers_df.drop(c_idx).reset_index(drop=True)
                            customers_df.to_csv("paid_customers.csv", index=False)
                            st.success("Customer record deleted.")
                            st.rerun()

                    inv_email = str(sel_cust["Email"]) if "Email" in sel_cust and pd.notna(sel_cust["Email"]) else "user@agentflow.ai"
                    inv_plan = str(sel_cust["Plan"]) if "Plan" in sel_cust and pd.notna(sel_cust["Plan"]) else "Pro"
                    inv_amt = str(sel_cust["Amount"]) if "Amount" in sel_cust and pd.notna(sel_cust["Amount"]) else "₹2,999"
                    inv_data = generate_invoice_pdf(inv_email, inv_plan, inv_amt)
                    st.download_button("📄 Download Customer Invoice", data=inv_data, file_name=f"invoice_{inv_email}.txt", mime="text/plain", key=f"dl_inv_admin_{c_idx}")
            else:
                st.info("No data available.")

        with crm_tab5:
            st.subheader("📈 Revenue, Leads, and Users Analytics")
            
            col_an1, col_an2 = st.columns(2)
            with col_an1:
                st.markdown("#### Revenue Growth")
                if not customers_df.empty and "Amount" in customers_df.columns:
                    try:
                        chart_cust = customers_df.copy()
                        chart_cust["Amount"] = chart_cust["Amount"].astype(str).str.replace("₹", "").str.replace(",", "").str.strip().astype(float)
                        if "Date" in chart_cust.columns:
                            st.line_chart(chart_cust, x="Date", y="Amount")
                        else:
                            st.line_chart(chart_cust["Amount"])
                    except Exception:
                        st.info("No data available.")
                else:
                    st.info("No data available.")

                st.markdown("#### Monthly Platform Users Growth")
                if not users_df.empty:
                    try:
                        if "Date" in users_df.columns:
                            st.bar_chart(users_df, x="Date")
                        else:
                            st.bar_chart(users_df)
                    except Exception:
                        st.info("No data available.")
                else:
                    st.info("No data available.")

            with col_an2:
                st.markdown("#### Leads Conversion Breakdown")
                if not leads_df.empty and "Status" in leads_df.columns:
                    try:
                        status_counts = leads_df["Status"].value_counts()
                        if not status_counts.empty:
                            st.bar_chart(status_counts)
                        else:
                            st.info("No data available.")
                    except Exception:
                        st.info("No data available.")
                else:
                    st.info("No data available.")

                st.markdown("#### Total Bookings Overview")
                if not bookings_df.empty:
                    try:
                        if "Submission Date" in bookings_df.columns:
                            st.bar_chart(bookings_df, x="Submission Date")
                        else:
                            st.bar_chart(bookings_df)
                    except Exception:
                        st.info("No data available.")
                else:
                    st.info("No data available.")
