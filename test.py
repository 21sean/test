import json
import streamlit as st
from streamlit_elements import elements, mui
import re

# Define default columns
DEFAULT_COLUMNS = [
    { "field": 'name', "headerName": 'Name', "width": 150, "editable": True },
    { "field": 'address', "headerName": 'Address', "width": 150, "editable": True },
]

# Function to handle cell edit events (optional)
def handle_edit(params):
    print(params)

# Function to handle search text change
def on_search_change(event):
    st.session_state['search_text'] = event.target.value
    st.experimental_rerun()  # Force the app to rerun to update the data grid

# Main function to display the DataGrid
def display_data_grid(kg):
    # Get the search text from session state or initialize it
    search_text = st.session_state.get('search_text', '')

    # Sanitize the search text to prevent injection attacks
    safe_search_text = re.sub(r"['\"\\\\]", '', search_text)

    # Construct the query with the sanitized search text
    query_string = f"""
    MATCH (users:User)
    WHERE users.name CONTAINS '{safe_search_text}'
    RETURN users LIMIT 5
    """

    # Query Neo4j
    data = kg.query(query_string)

    # Process the data to fit the DataGrid format
    processed_data = []
    for record in data:
        user = record['users']
        # Assuming 'user' is a dictionary-like object
        processed_data.append({
            'id': user.get('id', ''),  # Ensure a unique 'id' field
            'name': user.get('name', ''),
            'address': user.get('address', ''),
        })

    # Render the UI components
    with elements("data_grid"):
        with mui.Paper(
            sx={
                "display": "flex",
                "flexDirection": "column",
                "borderRadius": 3,
                "overflow": "hidden"
            },
            elevation=1
        ):
            # Title Bar
            with mui.Box(
                sx={
                    "padding": "10px 15px",
                    "display": "flex",
                    "alignItems": "center",
                    "backgroundColor": "#f5f5f5"
                }
            ):
                mui.icon.ViewCompact()
                mui.Typography("Data Grid", variant="h6", sx={"marginLeft": "10px"})

            # Search Box
            mui.TextField(
                label="Search by Name",
                defaultValue=search_text,
                onChange=on_search_change,
                sx={"margin": "10px"}
            )

            # Data Grid
            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                mui.DataGrid(
                    columns=DEFAULT_COLUMNS,
                    rows=processed_data,
                    pageSize=5,
                    rowsPerPageOptions=[5],
                    checkboxSelection=True,
                    disableSelectionOnClick=True,
                    onCellEditCommit=handle_edit,
                )
