import json
import streamlit as st
from streamlit_elements import elements, mui, lazy
import re

# Define default columns
DEFAULT_COLUMNS = [
    { "field": 'name', "headerName": 'Name', "width": 150, "editable": True },
    { "field": 'address', "headerName": 'Address', "width": 150, "editable": True },
]

# Function to handle cell edit events (optional)
def handle_edit(params):
    print(params)

# Main function to display the DataGrid
def display_data_grid(kg):
    # Initialize search text in session state if not present
    if 'search_text' not in st.session_state:
        st.session_state['search_text'] = ''
    if 'search_triggered' not in st.session_state:
        st.session_state['search_triggered'] = False

    # Render the UI components
    with elements("data_grid"):
        # Use lazy mode to prevent immediate rerendering
        with lazy(mode='manual'):
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

                # Search Box and Button
                with mui.Box(sx={"display": "flex", "alignItems": "center", "padding": "10px"}):
                    mui.TextField(
                        label="Search by Name",
                        defaultValue=st.session_state['search_text'],
                        onChange=lambda event: st.session_state.update({'search_text': event.target.value}),
                        sx={"marginRight": "10px", "flex": 1}
                    )
                    mui.Button(
                        "Search",
                        variant="contained",
                        onClick=lambda: st.session_state.update({'search_triggered': True})
                    )

                # If search has been triggered, perform the query
                if st.session_state['search_triggered']:
                    # Reset the trigger
                    st.session_state['search_triggered'] = False

                    # Sanitize the search text to prevent injection attacks
                    search_text = st.session_state['search_text']
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
                else:
                    # Placeholder or empty data grid
                    with mui.Box(sx={"flex": 1, "minHeight": 0}):
                        mui.Typography("Enter a search term and click 'Search' to display results.", sx={"padding": "20px"})

            # Commit the lazy elements after all updates
            lazy.next()

# Example usage
# Assuming 'kg' is your Neo4jGraph connection object
# display_data_grid(kg)
