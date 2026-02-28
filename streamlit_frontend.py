import streamlit as st
from langGraph_backend import chatbot
from langchain_core.messages import HumanMessage    


# definiing a config
CONFIG = {
    'configurable':{'thread_id': 'thread_1'}
}

# creating a dictionary to store the conversation history that would have  role and content and storing them in a list
# message_history = []
# instead of the above will use session state to store the message_history 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    
    # adding the user message to the message history
    st.session_state['message_history'].append({
        'role': 'user',
        'content': user_input
    })

    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({
            'messages': [HumanMessage(content=user_input)]},
            config=CONFIG
        )
    ai_response = response['messages'][-1].content
    
        # adding the ai response message to the message history
    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_response
    })
    with st.chat_message('assistant'):
        st.text(ai_response)