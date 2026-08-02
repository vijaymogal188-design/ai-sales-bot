import streamlit as st
import pandas as pd
import os
from groq import Groq
from datetime import datetime

# Page configuration
st.set_page_config(page_title="AI Business Employee", page_icon="🤖", layout="centered")

st.title("🤖 AI Business Employee")
st.write("Aapki service mein haazir!")

# Initialize Groq Client securely
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# System Prompt - The Brain of the Salesman
SYSTEM_PROMPT = """You are an expert AI Sales Agent. Your goal is to naturally converse with the user and collect exactly these 6 details:
1. Name
2. Business Name
3. Service Required
4. Budget
5. Phone Number
6. Email Address

RULES:
- Ask for these details conversationally, one or two at a time. Be polite and professional.
- Do not ask for all details at once. Do not show them a list.
- Once you have successfully collected ALL 6 details, you MUST stop the conversation and output EXACTLY this format and absolutely nothing else:
COMPLETE: Name | Business | Service | Budget | Phone | Email
Example: COMPLETE: Rahul | Tech Solutions | Web Design | 50000 | 9876543210 | rahul@email.com
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.messages.append({"role": "assistant", "content": "Hello! Welcome to our service. To get started, could you please tell me your name?"})

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
                model="llama3-8b-8192",
                temperature=0.5
            )
            
            response_text = chat_completion.choices[0].message.content
            
            # 🚨 MAGIC HAPPENS HERE: Check if AI sent the secret completion code
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
            st.error(f"Thoda error aa gaya bhai: {e}")
