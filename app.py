import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

# Page configuration
st.set_page_config(page_title="AgentFlow AI | Enterprise Sales Agent", page_icon="⚡", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    .hero-title {
        font-size: 40px;
        font-weight: 800;
        color: #0f172a;
        text-align: center;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #64748b;
        text-align: center;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown('<div class="hero-title">Scale Your Growth with AgentFlow AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Experience lightning-fast client acquisition and intelligent conversational sales.</div>', unsafe_allow_html=True)

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
