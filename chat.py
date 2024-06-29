from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

# Function to get response from the AI model
def get_response(user_query, chat_history):
    llm = ChatOllama(model="mistral")

    template = """
        You are a helpful assistant. 
        Answer the following questions considering the history of the conversation:
        Chat history: {chat_history}
        User question: {user_question}
        """
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query
    })

# Function to handle login
def login(username, password):
    if username in st.session_state.user_data and st.session_state.user_data[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
    else:
        st.error("Invalid username or password")

# Function to handle signup
def signup(username, password):
    if username in st.session_state.user_data:
        st.error("Username already exists")
    else:
        st.session_state.user_data[username] = password
        st.success("Signup successful! Please log in.")

# Function to display the login form
def login_form():
    st.header("Login to Lucid-CHATS")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        login(username, password)
    if st.button("Sign up"):
        st.session_state.signup = True

# Function to display the signup form
def signup_form():
    st.header("Sign up for Lucid-CHATS")
    username = st.text_input("Choose a Username", key="signup_username")
    password = st.text_input("Choose a Password", type="password", key="signup_password")
    if st.button("Create Account"):
        signup(username, password)
    if st.button("Back to Login"):
        st.session_state.signup = False

# Set up the Streamlit app
st.set_page_config(page_title="LucidCHATS😁", page_icon="🤖", layout="wide")
st.title("Lucid-CHATS😁")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "signup" not in st.session_state:
    st.session_state.signup = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi, I'm Husn bot, created by San. He is a chess player and GenAI enthusiast. How can I help you?")
    ]
if "questions" not in st.session_state:
    st.session_state.questions = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# Display the appropriate form based on session state
if not st.session_state.logged_in:
    if st.session_state.signup:
        signup_form()
    else:
        login_form()
else:
    # Sidebar with information and selectbox for stored questions
    st.sidebar.header("Lucid-CHATS Information")
    st.sidebar.info("Lucid-CHATS is a ChatGPT clone created with Mistral AI from Ollama and LangChain for orchestration. It aims to provide a helpful assistant experience.")

    # Display stored questions in a selectbox
    st.sidebar.subheader("Stored Questions")
    selected_question = st.sidebar.selectbox("Select a question to re-ask:", st.session_state.questions)

    # Display chat messages
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(f"**🤖 AI:** {message.content}")
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(f"**🧑 Human:** {message.content}")

    # User input
    user_query = st.chat_input("Type your message here...")

    if user_query:
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.questions.append(user_query)  # Add question to the stored questions list

        with st.chat_message("Human"):
            st.markdown(f"**🧑 Human:** {user_query}")

        with st.chat_message("AI"):
            response = st.write_stream(get_response(user_query, st.session_state.chat_history))
            st.session_state.chat_history.append(AIMessage(content=response))

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<center>Created by San - A GenAI Enthusiast🎅</center>", unsafe_allow_html=True)

