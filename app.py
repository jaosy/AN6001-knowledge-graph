import streamlit as st
from chatbot import EduChatbot


def main():
    st.title("Educational Chatbot")
    st.write("Assisted by NLP and Knowledge Graphs 🤖")

    # Initialize chatbot and session states
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = EduChatbot()
        st.session_state.messages = []
        st.session_state.last_intent = None

        welcome_message = st.session_state.chatbot.generate_welcome_message()
        st.session_state.messages.append(welcome_message)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Display suggested follow-ups if available
    if st.session_state.last_intent:
        followups = st.session_state.chatbot.get_suggested_followup(
            st.session_state.last_intent
        )
        if followups:
            with st.container():
                st.write("You might also want to ask:")
                for followup in followups:
                    if st.button(followup):
                        prompt = followup
                        st.session_state.messages.append(
                            {"role": "user", "content": prompt}
                        )
                        response = st.session_state.chatbot.get_response(prompt)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                        st.rerun()

    # chat input
    if prompt := st.chat_input("Your question"):
        # add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # display user message
        with st.chat_message("user"):
            st.write(prompt)

        # get chatbot response
        response = st.session_state.chatbot.get_response(prompt)

        # update last intent
        intent = st.session_state.chatbot._find_intent(prompt)
        if intent:
            st.session_state.last_intent = intent["name"]

        # add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # display assistant response
        with st.chat_message("assistant"):
            st.write(response)


if __name__ == "__main__":
    main()
