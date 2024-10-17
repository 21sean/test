import json
import streamlit as st
from streamlit_elements import elements, mui

# Define default columns
DEFAULT_COLUMNS = [
    { "field": 'name', "headerName": 'Name', "width": 150, "editable": True },
    { "field": 'address', "headerName": 'Address', "width": 150, "editable": True },
]

# Function to handle cell edit events (optional)
def handle_edit(params):
    print(params)

# Function to handle search text change
def on_search_change(value):
    st.session_state['search_text'] = value

# Main function to display the DataGrid
def display_data_grid(kg):
    # Get the search text from session state or initialize it
    search_text = st.session_state.get('search_text', '')

    # Construct the query with the search text
    # Using parameterized queries for security
    query_string = """
    MATCH (users:User)
    WHERE users.name CONTAINS $name
    RETURN users LIMIT 5
    """

    # Query Neo4j with parameters
    data = kg.query(query_string, name=search_text)

    # Process the data to fit the DataGrid format
    processed_data = []
    for record in data:
        user = record['users']
        processed_data.append({
            'id': user.id,  # Assuming 'id' is the unique identifier
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

# Example usage
# Assuming 'kg' is your Neo4j connection object
# display_data_grid(kg)
