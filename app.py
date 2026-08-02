import streamlit as st
from groq import Groq

# 1. Website ki setting
st.set_page_config(page_title="AI Sales Agent", page_icon="🤖")
st.title("🤖 AI Business Employee")
st.write("Aapki service mein haazir!")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
system_prompt = """Aap ek bohot hi professional aur polite Sales Executive hain ek IT & Tech Agency ke.
Aapka kaam customer se unki requirement samajhna aur leads collect karna hai.

Neeche diye gaye steps ko STRICTLY follow karein. 
RULE #1: Ek baar mein sirf EK HI sawaal poochein. Saare sawaal ek sath kabhi na poochein.
RULE #2: Customer ke pichle jawab ko acknowledge karein aur fir agla sawaal poochein.
RULE #3: Hamesha Hinglish/Hindi mein baat karein aur polite rahein.

STEPS TO FOLLOW ONE-BY-ONE:
1. Customer ka swagat karein aur unka Naam poochein.
2. Unka Business ya industry kya hai, yeh poochein.
3. Unhe kaunsi Service chahiye (jaise Website, Logo, AI Chatbot, App), yeh poochein.
4. (CRITICAL) Customer jo service chune, uske hisaab se sirf ek specific follow-up sawaal poochein.
5. Unka Budget poochein. (Agar customer sirf "haan" ya ajeeb jawab de, toh unse exact amount ya budget range poochein. Jab tak budget amount ya figure na mile, agle step par na jayein.)
6. Unka Phone Number poochein.
7. Unka Email ID poochein.
8. Aakhir mein unhe dhanyavad kahein aur batayein ki hamari team jald hi unse contact karegi.
"""

# 4. Streamlit ki memory (Session State) set karna
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 5. Purane messages ko screen par dikhana (System prompt ko chhod kar)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Naya message lene ka box
prompt = st.chat_input("Apna message yahan likhein...")

if prompt:
    # Customer ka message screen par dikhao
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Message ko memory mein save karo
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # AI se jawab maango
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )
    
    ai_reply = response.choices[0].message.content
    
    # AI ka jawab screen par dikhao
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
        
    # AI ke jawab ko memory mein save karo
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
import json
import csv
import os

# --- LEAD SAVE KARNE KA CODE ---
st.write("---")
if st.button("🚀 Save Lead (Admin Only)"):
    with st.spinner("AI lead ki details nikal raha hai..."):
        # Chat history ko ek jagah jama karna
        chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        
        # AI ko JSON mein data nikalne ka prompt dena
        prompt = f"""
        Is chat history ko dhyan se padho aur customer ki details nikal kar sirf ek JSON dictionary do.
        Keys exact ye honi chahiye: "Name", "Business", "Service", "Budget", "Phone", "Email".
        Agar koi detail chat mein nahi hai, toh wahan "Not Provided" likhna. Sirf valid JSON format dena, aur koi extra text nahi.
        
        Chat History:
        {chat_text}
        """
        
        try:
            # Groq API ko call karna
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            # AI ke jawab ko samajhna
            lead_data = json.loads(response.choices[0].message.content)
            
            # Data ko leads.csv file mein save karna
            file_exists = os.path.isfile("leads.csv")
            with open("leads.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Agar nayi file hai toh pehle headings likho
                if not file_exists:
                    writer.writerow(["Name", "Business", "Service", "Budget", "Phone", "Email"])
                
                # Customer ka data likho
                writer.writerow([
                    lead_data.get("Name", "Not Provided"),
                    lead_data.get("Business", "Not Provided"),
                    lead_data.get("Service", "Not Provided"),
                    lead_data.get("Budget", "Not Provided"),
                    lead_data.get("Phone", "Not Provided"),
                    lead_data.get("Email", "Not Provided")
                ])
            
            st.success("Lead successfully leads.csv file mein save ho gayi! 🎉")
            st.json(lead_data) # Screen par bhi dikhayega ki kya save hua hai
            
        except Exception as e:
            st.error(f"Save karne mein error aaya: {e}")
