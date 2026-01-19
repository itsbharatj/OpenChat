import streamlit as st 
from chatbot import response

@st.cache_data
def get_response(prompt,rag): 
    return response(prompt,include_rag=rag)

## Initilize the chat messages: 
# print(st.session_state)

# with st.sidebar: 

if "messages" not in st.session_state:
    st.session_state.messages = [] ## No messages currently

if "context" not in st.session_state: 
    st.session_state.context = False

## Render all the past messages onto streamlit:
for message in st.session_state.messages: 
    with st.chat_message(message["user"]): 
        st.write(message["content"])


## New prompt

prompt = st.chat_input("Please enter your message")


rag_input = st.button("Would you like context?")
enable_rag = rag_input or st.session_state.context
st.session_state.context = enable_rag

with st.container(horizontal=True, horizontal_alignment="distribute"):
    "Context Active" if enable_rag else "Context Deactivated"

if prompt:
    _response = get_response(str(st.session_state)+prompt,rag=enable_rag)
    st.session_state.messages.append({"user":"user","content":prompt})
    st.session_state.messages.append({"user":"ai","content":_response})
    with st.chat_message("user"): 
        st.write(prompt)
    with st.chat_message('ai'):
        st.write(_response)