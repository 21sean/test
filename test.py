import streamlit as st
from streamlit_elements import elements, dashboard, mui, html, sync
import logging

# Constants for the app title and sidebar (assuming these are defined elsewhere in your code)
TITLE = "Your App Title"

def sidebar():
    # Your sidebar implementation
    pass

def free_questions_exhausted():
    # Your implementation
    return False

def user_supplied_openai_key_unavailable():
    # Your implementation
    return False

def track(event_name, action, data):
    # Your tracking implementation
    pass

def rag_agent_get_results(question):
    # Simulated agent response
    return {"output": f"Response to '{question}'"}

def decrement_free_questions():
    # Your implementation
    pass

def handle_feedback(score):
    last_bot_message = st.session_state["messages"][-1]["content"]
    track(
        "rag_demo",
        "feedback_submitted",
        {"score": score, "bot_message": last_bot_message},
    )
    # Update the UI without rerunning
    sync()

# App title
st.set_page_config(layout="wide")
st.markdown(TITLE, unsafe_allow_html=True)
sidebar()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "ai",
            "content": "This is a Proof of Concept application which shows how GenAI can be used with Neo4j to build and consume Knowledge Graphs using both vectors and structured data.\nSee the sidebar for more information!",
        },
    ]

# Create a dashboard layout
layout = [
    dashboard.Item("chat_box", 0, 0, 12, 8),  # id, x, y, width, height
]

# Use elements to render the dashboard
with elements("dashboard"):

    # Import React and useState
    from react import useState

    # Define the dashboard grid
    with dashboard.Grid(layout, draggableHandle=".draggable"):
        # Create a Paper component to hold the chat interface
        with mui.Paper(
            key="chat_box",
            elevation=3,
            sx={
                "padding": "16px",
                "height": "100%",
                "display": "flex",
                "flexDirection": "column",
                "backgroundColor": "#FFFFFF",
            },
        ):
            # Title bar with draggable handle
            mui.Typography(
                "Chat",
                variant="h6",
                className="draggable",
                sx={"marginBottom": "16px", "color": "black"},
            )

            # Chat messages area
            with mui.Box(sx={"flex": 1, "overflowY": "auto", "marginBottom": "16px"}):
                for index, message in enumerate(st.session_state.messages):
                    alignment = "flex-end" if message["role"] == "user" else "flex-start"
                    bgcolor = "#DCF8C6" if message["role"] == "user" else "#F1F0F0"
                    text_color = "black"
                    with mui.Box(
                        key=f"message_{index}",
                        sx={
                            "display": "flex",
                            "justifyContent": alignment,
                            "marginBottom": "8px",
                        },
                    ):
                        mui.Paper(
                            mui.Typography(
                                message["content"],
                                sx={"whiteSpace": "pre-wrap", "color": text_color},
                            ),
                            sx={
                                "padding": "8px",
                                "backgroundColor": bgcolor,
                                "maxWidth": "80%",
                            },
                        )
                # Display feedback after AI messages
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "ai":
                    # Emoji feedback inside the chat box using MUI components
                    with mui.Box(sx={"display": "flex", "justifyContent": "center", "marginTop": "8px"}):
                        mui.IconButton(
                            mui.Icon("thumb_up"),
                            color="primary",
                            onClick=lambda: handle_feedback(1)
                        )
                        mui.IconButton(
                            mui.Icon("thumb_down"),
                            color="secondary",
                            onClick=lambda: handle_feedback(-1)
                        )

            # User input area
            if free_questions_exhausted() and user_supplied_openai_key_unavailable():
                mui.Alert(
                    "Thank you for trying out the Neo4j Rag Demo. Please input your OpenAI Key in the sidebar to continue asking questions.",
                    severity="warning",
                )
            else:
                # Use React's useState to manage the input value locally
                user_input, set_user_input = useState("")

                # Input field and send button
                def handle_submit():
                    nonlocal user_input  # Access the user_input from the local state
                    user_input_stripped = user_input.strip()
                    if user_input_stripped != "":
                        track("rag_demo", "question_submitted", {"question": user_input_stripped})
                        st.session_state.messages.append(
                            {"role": "user", "content": user_input_stripped}
                        )

                        # Get agent response
                        agent_response = rag_agent_get_results(
                            question=user_input_stripped
                        )
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
                        set_user_input("")  # Clear input field

                        # Update the UI without rerunning
                        sync()

                def handle_key_press(event):
                    if event.key == 'Enter':
                        handle_submit()

                with mui.Box(sx={"display": "flex"}):
                    mui.TextField(
                        placeholder="Ask question on the SEC Filings",
                        fullWidth=True,
                        variant="outlined",
                        name="user_input",
                        value=user_input,
                        onChange=lambda e: set_user_input(e.target.value),
                        onKeyDown=handle_key_press,
                        sx={"flex": 1},
                        InputProps={"style": {"color": "black"}},
                    )
                    mui.Button(
                        "Send",
                        onClick=handle_submit,
                        variant="contained",
                        sx={"marginLeft": "8px"},
                    )

# If you have other components outside the chat box, you can include them here
