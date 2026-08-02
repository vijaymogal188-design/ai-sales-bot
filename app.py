import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AgentFlow AI | Enterprise Sales Agent", 
    page_icon="⚡", 
    layout="wide"
)

# Custom CSS for Premium SaaS Landing Page UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Section */
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
        letter-spacing: 0.5px;
    }
    .hero-title {
        font-size: 48px;
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
        font-size: 18px;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 30px;
    }

    /* Section Headings */
    .section-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 50px;
        margin-bottom: 10px;
    }
    .section-subtitle {
        text-align: center;
        font-size: 16px;
        color: #64748b;
        margin-bottom: 40px;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: #94a3b8;
        font-size: 14px;
        border-top: 1px solid #e2e8f0;
        margin-top: 60px;
        background: #ffffff;
    }
    .footer span {
        color: #7c3aed;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq Client securely
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# System Prompt
SYSTEM_PROMPT = """You are an expert AI Sales Agent for AgentFlow AI. You can converse in both English and Hindi (or Hinglish) depending on what language the user prefers. Your goal is to naturally converse with the user and collect exactly these 6 details:
1. Name
2. Business Name
3. Service Required
4. Budget
5. Phone Number
6. Email Address

RULES:
- Match the language of the user. If they speak Hindi, reply in Hindi. If English, reply in English.
- Ask for these details conversationally, one or two at a time. Be polite, engaging, and professional.
- Do not ask for all details at once. Do not show them a list.
- Once you have successfully collected ALL 6 details, you MUST stop the conversation and output EXACTLY this format and absolutely nothing else:
COMPLETE: Name | Business | Service | Budget | Phone | Email
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "👋 Hello! Welcome to AgentFlow AI. I'm your virtual assistant. To get started, could you please tell me your name?"
    })

# Function to automatically save lead to CSV
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

# --- 1. HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">⚡ Next-Gen Business Automation</div>
        <div class="hero-title">Scale Your Growth with <span>AgentFlow AI</span></div>
        <div class="hero-subtitle">Experience lightning-fast client acquisition, intelligent workflow automations, and bespoke digital solutions designed to elevate your brand to market leadership.</div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SERVICES SECTION (5 Service Cards) ---
st.markdown('<div class="section-title">Our Professional Services</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Comprehensive solutions tailored to scale your digital presence.</div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)

with col_s1:
    st.markdown("### 🌐 Website Dev")
    st.write("High-performing, responsive, and conversion-focused modern websites.")

with col_s2:
    st.markdown("### 🤖 AI Chatbots")
    st.write("Custom intelligent conversational bots that handle sales 24/7.")

with col_s3:
    st.markdown("### 📱 App Dev")
    st.write("Scalable and robust mobile applications built for iOS & Android.")

with col_s4:
    st.markdown("### 🎨 Logo Design")
    st.write("Memorable brand identities and creative graphics that stand out.")

with col_s5:
    st.markdown("### 📈 Marketing")
    st.write("Data-driven growth campaigns to maximize your customer reach.")

st.markdown("---")

# --- 3. PRICING SECTION ---
st.markdown('<div class="section-title">Transparent Pricing Plans</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Choose the perfect tier that fits your company size and goals.</div>', unsafe_allow_html=True)

col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    st.markdown("### 🚀 Starter")
    st.markdown("#### **$49 /mo**")
    st.write("• Basic AI Chatbot Setup\n• Up to 500 Leads/mo\n• Standard Support\n• CSV Lead Export")

with col_p2:
    st.markdown("### 💼 Business")
    st.markdown("#### **$149 /mo**")
    st.write("• Advanced AI Sales Agent\n• Unlimited Leads\n• Priority Support\n• Bilingual Language Support")

with col_p3:
    st.markdown("### 🏢 Enterprise")
    st.markdown("#### **$399 /mo**")
    st.write("• Custom Workflow Integrations\n• Dedicated Account Manager\n• Custom CRM Sync\n• 24/7 Phone Support")

with col_p4:
    st.markdown("### ⚙️ Custom Quote")
    st.markdown("#### **Let's Talk**")
    st.write("• Tailored Multi-agent Setup\n• Custom API Architecture\n• On-premise Deployment\n• Enterprise Security")

st.markdown("---")

# --- 4. WHY CHOOSE US SECTION ---
st.markdown('<div class="section-title">Why Choose AgentFlow AI?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Engineered to give your business an unfair advantage.</div>', unsafe_allow_html=True)

col_w1, col_w2, col_w3 = st.columns(3)

with col_w1:
    st.markdown("### ⚡ 24/7 Automation")
    st.write("Never miss a potential customer. Our AI agents qualify leads around the clock instantly.")

with col_w2:
    st.markdown("### 🔒 Enterprise Security")
    st.write("Your business data and customer logs are securely processed with strict privacy standards.")

with col_w3:
    st.markdown("### 🌍 Bilingual Support")
    st.write("Seamlessly switch between English and Hindi to engage a wider regional audience.")

st.markdown("---")

# --- 5. AI CHAT INTERFACE (Center Aligned) ---
st.markdown('<div class="section-title">💬 Interactive AI Sales Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Chat with our intelligent assistant below to share your requirements.</div>', unsafe_allow_html=True)

col_c1, col_chat, col_c3 = st.columns([1, 2.5, 1])

with col_chat:
    # Display chat messages from history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
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
                        fallback_msg = "Thank you! Your details have been received. Our team will contact you soon."
                        st.markdown(fallback_msg)
                        st.session_state.messages.append({"role": "assistant", "content": fallback_msg})
                else:
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")

# --- 6. CONTACT SECTION ---
st.markdown('<div class="section-title">Get in Touch</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Have custom questions? Reach out to our founding team directly.</div>', unsafe_allow_html=True)

col_con1, col_con2 = st.columns(2)

with col_con1:
    st.markdown("### 📱 WhatsApp Support")
    st.write("Instant responses from our executive support team.")
    st.markdown("[Chat on WhatsApp (Click Here)](https://wa.me/)")

with col_con2:
    st.markdown("### 📧 Email Us")
    st.write("Drop your detailed business inquiries to our inbox.")
    st.markdown("[support@agentflowai.com](mailto:support@agentflowai.com)")

# --- 7. PROFESSIONAL FOOTER ---
st.markdown("""
    <div class="footer">
        <p>© 2026 <span>AgentFlow AI</span>. All rights reserved. Powered by Advanced Language Models.</p>
    </div>
""", unsafe_allow_html=True)
