
#1 import streamlit and chatbot file
import streamlit as st 
import  bedrockBackend as chatBot 

st.title("Hi, Am you LLM chatbot!. Ask me Anything!") # **Modify this based on the title you want in want


if 'memory' not in st.session_state: 
    st.session_state.memory = chatBot.demo_memory() 


if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] 

for message in st.session_state.chat_history: 
    with st.chat_message(message["role"]): 
        st.markdown(message["text"]) 

#6 Enter the details for chatbot input box 
     
input_text = st.chat_input("You are talking to Claude 3") # **display a chat input box
if input_text: 
    
    with st.chat_message("user"): 
        st.markdown(input_text) 
    
    st.session_state.chat_history.append({"role":"user", "text":input_text}) 

    chat_response = chatBot.demo_conversation(input_text=input_text, memory=st.session_state.memory) #** replace with ConversationChain Method name - call the model through the supporting library
    
    with st.chat_message("assistant"): 
        st.markdown(chat_response) 
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) 