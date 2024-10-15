import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# Title of your app
st.title('Weather Widget App')

# Create a text input for the user to enter a city
city = st.text_input("Enter a city", "New York")

# Placeholder for the weather widget
placeholder = st.empty()

# Base URL for the weather widget (forecast7)
base_url = "https://forecast7.com/en/"

# If a city is entered, show the weather widget
if city:
    # Transform the city name into a URL-friendly format
    city_encoded = urllib.parse.quote(city.lower().replace(' ', '-'))

    # Create a formatted widget URL for the given city
    widget_url = f"{base_url}{city_encoded}/"

    # Generate the widget code
    widget_code = f"""
    <a class="weatherwidget-io" href="{widget_url}" data-label_1="{city.upper()}" data-label_2="WEATHER" data-days="3" data-theme="pure" style="display:block; width: 100%; height: 100px;">{city.upper()} WEATHER</a>
    <script>
    !function(d,s,id){{
      var js,fjs=d.getElementsByTagName(s)[0];
      if(!d.getElementById(id)){{
        js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';
        fjs.parentNode.insertBefore(js,fjs);
      }}
    }}(document,'script','weatherwidget-io-js');
    </script>
    """

    # Place the weather widget in the placeholder at the top
    with placeholder:
        components.html(widget_code, height=130)
