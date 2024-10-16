import streamlit as st
from streamlit_elements import elements, dashboard, mui

# App title
st.markdown(TITLE, unsafe_allow_html=True)
sidebar()

# Define message placeholder and emoji feedback placeholder
placeholder = st.empty()
emoji_feedback = st.empty()
user_placeholder = st.empty()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "content": f"This is a Proof of Concept application which shows how GenAI can be used with Neo4j to build and consume Knowledge Graphs using both vectors and structured data.\nSee the sidebar for more information!",
        },
    ]

# Create a dashboard layout
layout = [
    dashboard.Item("chat_box", 0, 0, 6, 8),  # id, x, y, width, height
]

# Use elements to render the dashboard
with elements("dashboard"):
    with dashboard.Grid(layout, draggableHandle=".draggable"):
        with mui.Paper(key="chat_box", elevation=3, sx={"padding": "16px"}):
            mui.Typography("Chat", variant="h6", className="draggable")

            # Display chat messages from history on app rerun
            with placeholder.container():
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"], unsafe_allow_html=True)

            # User input
            if free_questions_exhausted() and user_supplied_openai_key_unavailable():
                st.warning(
                    "Thank you for trying out the Neo4j Rag Demo. Please input your OpenAI Key in the sidebar to continue asking questions."
                )
                st.stop()

            if "sample" in st.session_state and st.session_state["sample"] is not None:
                user_input = st.session_state["sample"]
            else:
                user_input = st.chat_input(
                    placeholder="Ask question on the SEC Filings", key="user_input"
                )

            if user_input:
                with user_placeholder.container():
                    track("rag_demo", "question_submitted", {"question": user_input})
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    with st.chat_message("user"):
                        st.markdown(user_input)

                    with st.chat_message("ai"):
                        with st.spinner("..."):
                            message_placeholder = st.empty()
                            thought_container = st.container()

                            agent_response = rag_agent.get_results(
                                question=user_input, callbacks=[]
                            )

                            if not isinstance(agent_response, dict):
                                logging.warning(
                                    f"Agent response was not the expected dict type: {agent_response}"
                                )
                                agent_response = str(agent_response)

                            content = agent_response["output"]

                            track(
                                "rag_demo", "ai_response", {"type": "rag_agent", "answer": content}
                            )
                            new_message = {"role": "ai", "content": content}
                            st.session_state.messages.append(new_message)

                            decrement_free_questions()

                        message_placeholder.markdown(content)

                # Reinsert user chat input if sample quick select was previously used.
                if "sample" in st.session_state and st.session_state["sample"] is not None:
                    st.session_state["sample"] = None
                    user_input = st.chat_input(
                        placeholder="Ask question on the SEC Filings", key="user_input"
                    )

                emoji_feedback = st.empty()

            # Emoji feedback
            with emoji_feedback.container():
                feedback = streamlit_feedback(feedback_type="thumbs")
                if feedback:
                    score = feedback["score"]
                    last_bot_message = st.session_state["messages"][-1]["content"]
                    track(
                        "rag_demo",
                        "feedback_submitted",
                        {"score": score, "bot_message": last_bot_message},
                    )
