<p style="color: #64748b; font-size: 14px;">Share your requirements below and let our AI handle the rest instantly.</p>
        </div>
    """, unsafe_allow_html=True)
    
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
                
                # Check if AI sent the secret completion code
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

# --- MODERN FOOTER ---
st.markdown("""
    <div class="footer">
        <p>© 2026 <span>AgentFlow AI</span>. All rights reserved. Powered by Advanced Language Models.</p>
    </div>
""", unsafe_allow_html=True)
