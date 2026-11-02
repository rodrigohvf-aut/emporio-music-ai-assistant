import streamlit as st
from app.agent import EmporioAssistant

st.set_page_config(page_title="Emporio Music Assistant", page_icon="🎵")
st.title("Emporio Music AI Assistant")
st.caption("Customer-facing responses are in Brazilian Portuguese.")
assistant = EmporioAssistant()
if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages: st.chat_message(message["role"]).write(message["content"])
if prompt := st.chat_input("Como posso ajudar?"):
    st.session_state.messages.append({"role": "user", "content": prompt}); st.chat_message("user").write(prompt)
    answer = assistant.answer(prompt); st.session_state.messages.append({"role": "assistant", "content": answer}); st.chat_message("assistant").write(answer)
