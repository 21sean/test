# Ensure input_value and button_clicked are in session_state
if "input_value" not in st.session_state:
    st.session_state.input_value = ""
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# Move the chat into a streamlit-elements component
with elements("chat_box"):

    # Display chat messages from history
    for message in st.session_state.messages:
        if message["role"] == "user":
            mui.Typography(
                message["content"],
                align="left",
                sx={"marginBottom": 2, "textAlign": "left", "color": "blue"},
            )
        else:
            mui.Typography(
                message["content"],
                align="right",
                sx={"marginBottom": 2, "textAlign": "right", "color": "green"},
            )

    # Input area for new message
    with mui.Stack(direction="row", spacing=1):

        # Define event handlers
        def handle_input_change(event):
            st.session_state.input_value = event.target.value

        def handle_button_click(event):
            st.session_state.button_clicked = True

        mui.TextField(
            label="Ask question on the SEC Filings",
            fullWidth=True,
            variant="outlined",
            value=st.session_state.input_value,
            onChange=handle_input_change,
        )
        mui.Button(
            "Send",
            variant="contained",
            onClick=handle_button_click,
        )

# Handle send button click outside the elements context
if st.session_state.button_clicked:
    user_input = st.session_state.input_value
    if user_input:
        if free_questions_exhausted() and user_supplied_openai_key_unavailable():
            st.warning(
                "Thank you for trying out the Neo4j Rag Demo. Please input your OpenAI Key in the sidebar to continue asking questions."
            )
            st.stop()

        track("rag_demo", "question_submitted", {"question": user_input})
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Agent response
        with st.spinner("..."):
            agent_response = rag_agent.get_results(question=user_input, callbacks=[])

            if not isinstance(agent_response, dict):
                logging.warning(
                    f"Agent response was not the expected dict type: {agent_response}"
                )
                agent_response = {"output": str(agent_response)}

            content = agent_response["output"]

            track(
                "rag_demo",
                "ai_response",
                {"type": "rag_agent", "answer": content},
            )
            new_message = {"role": "ai", "content": content}
            st.session_state.messages.append(new_message)

            decrement_free_questions()

        # Clear input value and reset button clicked
        st.session_state.input_value = ""
        st.session_state.button_clicked = False

        # Rerun to update the chat
        st.experimental_rerun()

# Emoji feedback
feedback = streamlit_feedback(feedback_type="thumbs")
if feedback:
    score = feedback["score"]
    last_bot_message = st.session_state["messages"][-1]["content"]
    track(
        "rag_demo",
        "feedback_submitted",
        {"score": score, "bot_message": last_bot_message},
    )
