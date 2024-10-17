import json
import streamlit as st
from streamlit_elements import mui, elements, dashboard
from .dashboard import Dashboard

class DataGrid(Dashboard.Item):

    DEFAULT_COLUMNS = [
        { "field": 'name', "headerName": 'Name', "width": 150, "editable": True },
        { "field": 'address', "headerName": 'Address', "width": 150, "editable": True },
    ]

    def __init__(self, key, kg):
        super().__init__(key)
        self.kg = kg

    def _handle_edit(self, params):
        print(params)

    def _on_search_change(self, event):
        st.session_state['search_text'] = event.target.value

    def __call__(self):
        # Get the search text from session state or initialize it
        search_text = st.session_state.get('search_text', '')

        # Construct the query with the search text
        query_string = f"""
        MATCH (users:User)
        WHERE users.name CONTAINS '{search_text}'
        RETURN users LIMIT 5
        """

        # Query Neo4j
        data = self.kg.query(query_string)

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
        with mui.Paper(
            key=self._key,
            sx={
                "display": "flex",
                "flexDirection": "column",
                "borderRadius": 3,
                "overflow": "hidden"
            },
            elevation=1
        ):
            with self.title_bar(
                padding="10px 15px 10px 15px",
                dark_switcher=False
            ):
                mui.icon.ViewCompact()
                mui.Typography("Data Grid")

            # Search Box
            mui.TextField(
                label="Search by Name",
                value=search_text,
                onChange=self._on_search_change,
                sx={"margin": "10px"}
            )

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                mui.DataGrid(
                    columns=self.DEFAULT_COLUMNS,
                    rows=processed_data,
                    pageSize=5,
                    rowsPerPageOptions=[5],
                    checkboxSelection=True,
                    disableSelectionOnClick=True,
                    onCellEditCommit=self._handle_edit,
                )
