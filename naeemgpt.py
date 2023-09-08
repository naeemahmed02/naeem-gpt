import streamlit as st
import openai

st.title("Naeem GPT: Blog Generator")
st.markdown("Generate a blog by simply providing the topic you are intersted. This Naeem GPT will Generate a Seo optimized Blog.")

# openai.api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = "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"

if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input("Enter the Topic to Generate a Blog"):
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({'role' : 'user', 'content' : prompt})

    # Add system message to chat history
    system_message = """You are trained to analyze a topic and generate a blog post.
        The blog post must contain 1000 to 1200 words (No less than 700 words)."""
    st.session_state.messages.append({'role' : 'system', 'content' : system_message})

    user_message = f"""Analyze the topic and generate a blog post. The topic is {prompt}
        The blog post should contain the following format.
        1) Title (Not more than one line)
        2) Introduction (Give an introduction about the topic)
        3) Add an image URL relevant to the topic.
        4) Add 2/3 subheadings and explain them.
        5) Body (should describe the facts and findings)
        6) Add an image URL relevant to the topic.
        7) Add 2/3 subheadings and explain them.
        8) General FAQ regarding the topic.
        9) Conclusion of the topic."""
    
    # Split the user message into multiple system and user messages
    user_messages = user_message.split('\n')
    for message in user_messages:
        st.session_state.messages.append({'role' : 'user', 'content' : message.strip()})

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model = st.session_state['openai_model'],
            messages = [
                {"role" : m["role"], "content" : m['content']}
                for m in st.session_state.messages
            ],
            stream = True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder .markdown(full_response + "| ")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role" : "assistant", "content" : full_response})
