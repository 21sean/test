 # Right side: Sample questions (4 columns)
        with mui.Grid(item=True, xs=4):
            mui.Typography("Sample Questions", variant="h6", gutterBottom=True)
            with mui.Box(sx=sample_questions_style):
                # Display sample questions as buttons
                for idx, question in enumerate(SAMPLE_QUESTIONS):
                    def make_on_click(q=question):
                        def on_click():
                            # Append user message
                            st.session_state.messages.append({
                                "role": "user",
                                "content": q
                            })
                            # Get LLM response
                            response = get_llm_response(q)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response
                            })
                        return on_click

                    mui.Button(
                        question,
                        variant="outlined",
                        color="secondary",
                        fullWidth=True,
                        sx={"justifyContent": "flex-start", "marginTop": 1},
                        onClick=make_on_click()
                    )
