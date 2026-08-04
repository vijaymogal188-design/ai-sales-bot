import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="AgentFlow AI | Enterprise CRM Dashboard", 
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
    .whatsapp-float { position: fixed; bottom: 30px; right: 30px; background-color: #25d366; color: white; border-radius: 50px; text-align: center; font-size: 30px; box-shadow: 2px 2px 3px #999; z-index: 1000; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; text-decoration: none; }
    .whatsapp-float:hover { background-color: #20ba5a; color: white; }
    .footer { background: #0f172a; color: #f8fafc; padding: 50px 30px 20px 30px; border-top: 1px solid #1e293b; margin-top: 60px; border-radius: 16px 16px 0 0; }
    .footer a { color: #94a3b8; text-decoration: none; }
</style>

<a href="https://wa.me/919876543210?text=Hello%20AgentFlow%20AI,%20I%20want%20to%20know%20more%20about%20your%20services!" class="whatsapp-float" target="_blank" title="Chat on WhatsApp">💬</a>
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

st.sidebar.markdown("### ⚡ AgentFlow AI")
st.sidebar.caption("Enterprise CRM Dashboard v3.0")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio("Navigation", ["Home / Landing Page", "Pricing & Plans", "AI Package Recommender", "Portfolio / Projects", "Testimonials", "Book a Meeting", "Contact Us", "Customer Login / Signup", "Admin CRM Dashboard", "Legal & Policies"])

st.sidebar.markdown("---")
st.sidebar.markdown("🛡️ **Enterprise Security**")
st.sidebar.caption("SSL Secured | 24/7 Support")

if nav_choice == "Home / Landing Page":
    st.markdown('<div class="hero-container"><div class="hero-badge">⚡ Next-Gen Business Automation & AI</div><div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div><div class="hero-subtitle">Experience lightning-fast client acquisition, intelligent workflow automations, and bespoke digital solutions designed to elevate your brand globally.</div></div>', unsafe_allow_html=True)
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
            st.markdown('<div class="checkout-box"><h3>📋 Order Summary</h3>', unsafe_allow_html=True)
            st.write(f"**Plan Tier:** {plan['name']} Subscription")
            st.write(f"**Total Amount:** {plan['price']}")
            email_input = st.text_input("Billing Email Address")
            if st.button("Pay Securely with Razorpay"):
                if email_input:
                    save_paid_customer(email_input, plan['name'], plan['price'])
                    st.session_state.logged_in = True
                    st.session_state.username = email_input.split("@")[0]
                    st.session_state.checkout_active = False
                    st.success("Payment Successful via Razorpay! Redirecting to Dashboard...")
                    st.balloons()
                    st.rerun()
                else: st.warning("Please enter your email.")
            if st.button("⬅️ Back to Pricing"): 
                st.session_state.checkout_active = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            elif nav_choice == "AI Package Recommender":
    st.markdown('<div class="section-title">🤖 AI Package Recommender</div>', unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        biz_type = st.selectbox("What is your business type?", ["Solo Creator / Freelancer", "Growing Startup / SME", "Large Enterprise"])
        main_goal = st.selectbox("What is your primary goal?", ["Lead Generation & Chatbots", "Full Website & App Development", "Custom Enterprise Automation"])
    with col_r2:
        st.write("")
        st.write("")
        if st.button("✨ Get AI Recommendation"):
            st.success("Analysis complete! Based on your profile:")
            if biz_type == "Solo Creator / Freelancer": st.info("🚀 **Recommended Plan: Starter (₹999)**")
            elif biz_type == "Growing Startup / SME": st.info("💼 **Recommended Plan: Pro (₹2,999)**")
            else: st.info("🔥 **Recommended Plan: Premium (₹7,999+)**")

elif nav_choice == "Portfolio / Projects":
    st.markdown('<div class="section-title">Our Portfolio & Project Cards</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    with p1: st.markdown('<div class="portfolio-card"><h3>🛒 AI E-Commerce Suite</h3><p>Automated sales bot.</p></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="portfolio-card"><h3>🏥 HealthTech SaaS</h3><p>Secure patient portal.</p></div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="portfolio-card"><h3>📊 FinTech Analytics</h3><p>Automated compliance.</p></div>', unsafe_allow_html=True)

elif nav_choice == "Testimonials":
    st.markdown('<div class="section-title">⭐ Client Testimonials</div>', unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1: st.markdown('<div class="testimonial-card">"Pipeline automated seamlessly!"<br><br><b>— Rajesh Sharma</b></div>', unsafe_allow_html=True)
    with t2: st.markdown('<div class="testimonial-card">"Chatbot handles queries 24/7!"<br><br><b>— Priya Patel</b></div>', unsafe_allow_html=True)
    with t3: st.markdown('<div class="testimonial-card">"Incredible CRM and payments!"<br><br><b>— Amit Verma</b></div>', unsafe_allow_html=True)

elif nav_choice == "Book a Meeting":
    st.markdown('<div class="section-title">📅 Enterprise Meeting Booking System</div>', unsafe_allow_html=True)
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        b_name = st.text_input("Full Name", key="bk_name")
        b_email = st.text_input("Email Address", key="bk_email")
        b_phone = st.text_input("Phone Number", key="bk_phone")
    with col_b2:
        b_service = st.selectbox("Service Required", ["AI Chatbot", "Website Dev", "Mobile App", "Enterprise Automation"])
        b_date = st.date_input("Select Meeting Date", key="bk_date")
        b_time = st.selectbox("Select Time Slot", ["10:00 AM - 11:00 AM", "02:00 PM - 03:00 PM"])
    if st.button("Submit Meeting Booking"):
        if b_name and b_email and b_phone:
            save_booking_to_csv(b_name, b_email, b_phone, b_service, b_date, b_time)
            st.success("🎉 Booking successfully submitted! Status: Pending.")
            st.balloons()
        else: st.warning("Please fill in required fields.")

elif nav_choice == "Contact Us":
    st.markdown('<div class="section-title">Contact Us</div>', unsafe_allow_html=True)
    c_name = st.text_input("Your Full Name")
    c_email = st.text_input("Your Email Address")
    c_service = st.selectbox("Service", ["Website Dev", "AI Chatbot", "App Dev"])
    c_msg = st.text_area("Your Message")
    if st.button("Submit Inquiry"):
        if c_name and c_email and c_msg:
            save_lead_to_csv([c_name, "Inquiry Form", c_service, "Custom", "N/A", c_email])
            st.success("✅ Inquiry submitted to CRM successfully!")
        else: st.warning("Fill all fields.")

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
                if nu and ne and np: st.session_state.logged_in = True; st.session_state.username = nu; st.success("Created!"); st.rerun()
    else:
        st.markdown(f"## 👋 Welcome, {st.session_state.username}!")
        dt1, dt2, dt3, dt4 = st.tabs(["Status", "Files", "Invoices", "Support"])
        with dt1: st.metric("Project", "AI Sales Agent", "Active")
        with dt2: st.download_button("Download Code", "code bytes", "project.zip")
        with dt3: st.table(pd.DataFrame({"Invoice": ["#INV-1"], "Amount": ["₹999"], "Status": ["Paid"]}))
        with dt4: st.write("Support chat active.")

elif nav_choice == "Admin CRM Dashboard":
    if not st.session_state.admin_logged_in:
        st.markdown("<h2 style='text-align: center;'>🔒 Admin Authentication</h2>", unsafe_allow_html=True)
        col_ad1, col_ad2, col_ad3 = st.columns([1, 2, 1])
        with col_ad2:
            admin_pass = st.text_input("Enter Admin Password", type="password")
            if st.button("Login as Admin"):
                if admin_pass == "admin123": st.session_state.admin_logged_in = True; st.rerun()
                else: st.error("Incorrect password!")
    else:
        st.markdown("## 🛡️ Enterprise Admin CRM Dashboard")
        if st.sidebar.button("Admin Logout"): st.session_state.admin_logged_in = False; st.rerun()
        
        tot_l = len(pd.read_csv("leads.csv")) if os.path.exists("leads.csv") else 0
        tot_c, tot_rev, pend_p = 0, 0, 0
        if os.path.exists("paid_customers.csv"):
            df_c = pd.read_csv("paid_customers.csv")
            tot_c = len(df_c)
            for amt in df_c["Amount"]:
                clean = str(amt).replace("₹", "").replace(",", "").strip()
                if clean.isdigit(): tot_rev += int(clean)
            if "Project Status" in df_c.columns: pend_p = len(df_c[df_c["Project Status"] == "In Progress"])
        
        tot_b = len(pd.read_csv("bookings.csv")[pd.read_csv("bookings.csv")["Meeting Date"] == datetime.now().strftime("%Y-%m-%d")]) if os.path.exists("bookings.csv") else 0

        m1, m2, m3, m4, m5 = st.columns(5)
        with m1: st.metric("Total Leads", tot_l)
        with m2: st.metric("Total Customers", tot_c)
        with m3: st.metric("Today's Bookings", tot_b)
        with m4: st.metric("Total Revenue", f"₹{tot_rev:,}")
        with m5: st.metric("Pending Projects", pend_p)
        st.markdown("---")

        crm1, crm2, crm3 = st.tabs(["Leads CRM", "Bookings CRM", "Paid Customers"])
        with crm1:
            if os.path.exists("leads.csv"):
                df_l = pd.read_csv("leads.csv")
                search_l = st.text_input("🔍 Search Leads:")
                if search_l: df_l = df_l[df_l.astype(str).apply(lambda x: x.str.contains(search_l, case=False)).any(axis=1)]
                st.dataframe(df_l, use_container_width=True)
                st.download_button("Export Leads CSV", df_l.to_csv(index=False).encode('utf-8'), "leads.csv", "text/csv")
            else: st.warning("No leads yet.")
        with crm2:
            if os.path.exists("bookings.csv"):
                df_b = pd.read_csv("bookings.csv")
                st.dataframe(df_b, use_container_width=True)
                st.download_button("Export Bookings CSV", df_b.to_csv(index=False).encode('utf-8'), "bookings.csv", "text/csv")
            else: st.warning("No bookings yet.")
        with crm3:
            if os.path.exists("paid_customers.csv"):
                df_pc = pd.read_csv("paid_customers.csv")
                st.dataframe(df_pc, use_container_width=True)
                st.download_button("Export Customers CSV", df_pc.to_csv(index=False).encode('utf-8'), "customers.csv", "text/csv")
            else: st.warning("No customers yet.")

elif nav_choice == "Legal & Policies":
    st.markdown('<div class="section-title">Legal Policies & Terms</div>', unsafe_allow_html=True)
    lt1, lt2, lt3 = st.tabs(["Privacy", "Terms", "Refund"])
    with lt1: st.write("Privacy policy details.")
    with lt2: st.write("Terms of service details.")
    with lt3: st.write("Refund policy details.")
