import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#***************************************************Utility Fuction*************************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id ()
    st.session_state['thread_id']= thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']= []

# def add_thread(thread_id):
#     if thread_id not in st.session_state['chat_threads']:
#         st.session_state['chat_threads'].append(thread_id)

def add_thread(thread_id):
    st.session_state['chat_threads'].append(
        {
            "thread_id": thread_id,
            "title": "New Chat"
        }
    )

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )

    return state.values.get('messages', [])

#**********************************************************Session Startup********************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] =[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []



#************************************Sidebar UI*****************************
st.sidebar.title('LangGraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()

# st.sidebar.header('My Conversations')
# for thread_id in st.session_state['chat_threads'][::-1]:
#     if st.sidebar.button(str(thread_id)):
#         st.session_state['thread_id'] = thread_id
#         messages = load_conversation(thread_id)

#         temp_messages =[]
#         for message in messages:
#             if isinstance(message,HumanMessage):
#                 role = 'user'
#             else:
#                 role = 'assistant'
#             temp_messages.append({'role':role, 'content':message.content})
#         st.session_state['message_history'] = temp_messages
st.sidebar.header('My Conversations')

for thread in st.session_state['chat_threads'][::-1]:
      if st.sidebar.button(thread['title'], key=str(thread['thread_id'])):

    # if st.sidebar.button(thread['title']):
        st.session_state['thread_id'] = thread['thread_id']
        messages = load_conversation(thread['thread_id'])

        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            temp_messages.append(
                {'role': role, 'content': message.content}
            )
            

        st.session_state['message_history'] = temp_messages





#***************************************Main UI********************************
# for loading the conversation history
# for message in st.session_state['message_history']:
#     with st.chat_message(message['role']):
#         st.text(message['content'])

# user_input = st.chat_input('Type here...')
# if user_input:

#     with st.chat_message('user'):
#         st.text(user_input)

#     CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}

#     st.session_state['message_history'].append(
#         {'role': 'user', 'content': user_input}


#     )
#  ##AI   
# for thread in st.session_state['chat_threads']:
#     if thread['thread_id'] == st.session_state['thread_id']:
#         if thread['title'] == 'New Chat':fg
#             thread['title'] = user_input[:30]
#         break



#***************************************Main UI********************************
# for loading the conversation history
#AI CODE
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here...')

if user_input:

    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {
        'configurable': {
            'thread_id': st.session_state['thread_id']
        }
    }

    st.session_state['message_history'].append(
        {
            'role': 'user',
            'content': user_input
        }
    )

    # Update conversation title (only for the first message)
    for thread in st.session_state['chat_threads']:
        if thread['thread_id'] == st.session_state['thread_id']:
            if thread['title'] == 'New Chat':
                thread['title'] = user_input[:30]
            break

    # AI Response
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append(
        {
            'role': 'assistant',
            'content': ai_message
        }
    )



    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append(
        {'role': 'assistant', 'content': ai_message}
    )