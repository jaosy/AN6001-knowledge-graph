import streamlit as st
from chatbot import EduChatbot

def main():
    st.title("Educational Chatbot")
    st.write("Assisted by NLP and Knowledge Graphs 🤖")

    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = EduChatbot()

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": """
                    👋 Hello! I'm your Educational Analytics Assistant.

                    I can help you analyze:
                    
                    • Module transitions and student performance
                    
                    • Similar students and common mistake patterns
                    
                    • Module prerequisites and relationships

                    Try asking me questions like:
                    1. "How are students performing between modules?"
                    2. "Find similar students and their patterns"
                    3. "Show me module prerequisites"

                    How can I help you today?
                """
            }
        )

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Your question"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get chatbot response
        response = st.session_state.chatbot.get_response(prompt)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()