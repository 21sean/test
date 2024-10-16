with mui.Paper(key="chat_box", elevation=3, sx={"padding": "16px", "height": "100%", "display": "flex", "flexDirection": "column"}):
            # Title bar with draggable handle
            mui.Typography("Chat", variant="h6", className="draggable", sx={"marginBottom": "16px"})

            # Chat messages area
            with mui.Box(sx={"flex": 1, "overflowY": "auto", "marginBottom": "16px"}):
                for index, message in enumerate(st.session_state.messages):
                    with mui.Box(key=f"message_{index}", sx={"display": "flex", "justifyContent": "flex-end" if message["role"] == "user" else "flex-start", "marginBottom": "8px"}):
                        mui.Paper(
                            mui.Typography(message["content"], sx={"whiteSpace": "pre-wrap"}),
                            sx={
                                "padding": "8px",
                                "backgroundColor": "#DCF8C6" if message["role"] == "user" else "#F1F0F0",
                                "maxWidth": "80%",
                            }
                        )

            # User input area
            if free_questions_exhausted() and user_supplied_openai_key_unavailable():
                mui.Alert(
                    "Thank you for trying out the Neo4j Rag Demo. Please input your OpenAI Key in the sidebar to continue asking questions.",
                    severity="warning"
                )
            else:
                # Input field and send button
                def handle_send():
                    user_input = st.session_state.get("user_input", "").strip()
                    if user_input != "":
                        track("rag_demo", "question_submitted", {"question": user_input})
                        st.session_state.messages.append({"role": "user", "content": user_input})

                        # Get agent response
                        agent_response = rag_agent.get_results(question=user_input, callbacks=[])
                        if not isinstance(agent_response, dict):
                            logging.warning(
                                f"Agent response was not the expected dict type: {agent_response}"
                            )
                            agent_response = {"output": str(agent_response)}
                        content = agent_response["output"]
                        track(
                            "rag_demo", "ai_response", {"type": "rag_agent", "answer": content}
                        )
                        new_message = {"role": "ai", "content": content}
                        st.session_state.messages.append(new_message)

                        decrement_free_questions()
                        st.session_state.user_input = ""  # Clear input field

                        # Rerun to update the chat messages
                        st.experimental_rerun()

                with mui.Box(sx={"display": "flex"}):
                    mui.TextField(
                        placeholder="Ask question on the SEC Filings",
                        fullWidth=True,
                        variant="outlined",
                        value=st.session_state.get("user_input", ""),
                        onChange=lambda e: st.session_state.update({"user_input": e.target.value}),
                        onKeyDown=lambda e: handle_send() if e.key == 'Enter' else None,
                        sx={"flex": 1}
                    )
                    mui.Button("Send", variant="contained", onClick=handle_send, sx={"marginLeft": "8px"})

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
