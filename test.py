import streamlit as st
import streamlit.components.v1 as components

# Title of your app
st.title('Weather Widget App')

# Create a text input for the user to enter a city
city = st.text_input("Enter a city", "New York")

# Base URL for the weather widget (forecast7)
base_url = "https://forecast7.com/en/"

# You may need to transform the city name into a URL-friendly format.
# For simplicity, we will not handle encoding for now, but if needed, you can add that logic.

# Placeholder for the weather widget
placeholder = st.empty()

# If a city is entered, show the weather widget
if city:
    # Format the widget URL based on the city input (you can customize this based on your preferred weather service)
    widget_code = f"""
    <a class="weatherwidget-io" href="{base_url}40d71n74d01/{city.lower().replace(' ', '-')}/" data-label_1="{city.upper()}" data-label_2="WEATHER" data-days="3" data-theme="pure" style="display:block; width: 300px; height: 100px;" >{city.upper()} WEATHER</a>
    <script>
    !function(d,s,id){
      var js,fjs=d.getElementsByTagName(s)[0];
      if(!d.getElementById(id)){
        js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';
        fjs.parentNode.insertBefore(js,fjs);
      }
    }(document,'script','weatherwidget-io-js');
    </script>
    """

    # Place the weather widget in the placeholder at the top
    with placeholder:
        components.html(widget_code, height=100, width=300)

# Additional content for your app can go here
st.write("This is the rest of the app content.")
