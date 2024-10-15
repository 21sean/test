import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
0ce2695c3850437fabc220852241510
import streamlit as st
import requests

# -------------------------------
# Configuration
# -------------------------------

# Replace with your actual API key
WEATHERAPI_KEY = 'YOUR_WEATHERAPI_KEY'  # WeatherAPI.com API Key

# Default location set to China
DEFAULT_LOCATION = 'China'

# -------------------------------
# Helper Functions
# -------------------------------

def get_location_suggestions(query):
    """
    Get location suggestions from the WeatherAPI.com Search API based on the user's query.
    """
    if not query:
        return []
    
    url = f'http://api.weatherapi.com/v1/search.json?key={WEATHERAPI_KEY}&q={query}'
    response = requests.get(url)
    suggestions = []
    if response.status_code == 200:
        data = response.json()
        for item in data:
            name = item.get('name')
            region = item.get('region')
            country = item.get('country')
            lat = item.get('lat')
            lon = item.get('lon')
            display_name = f"{name}, {region}, {country}" if region else f"{name}, {country}"
            suggestions.append({
                'display_name': display_name,
                'lat': lat,
                'lon': lon
            })
    return suggestions

def get_weather(lat, lon):
    """
    Get weather data from WeatherAPI.com based on latitude and longitude.
    """
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={lat},{lon}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def display_weather_info(weather_data, location_name):
    """
    Display weather information in the Streamlit app.
    """
    st.subheader(f"Weather in {location_name}")
    col1, col2 = st.columns(2)
    with col1:
        temp_c = weather_data['current']['temp_c']
        feelslike_c = weather_data['current']['feelslike_c']
        st.metric("Temperature", f"{temp_c} °C", f"Feels like {feelslike_c} °C")
        humidity = weather_data['current']['humidity']
        st.write(f"**Humidity:** {humidity}%")
    with col2:
        condition = weather_data['current']['condition']['text']
        icon_url = f"http:{weather_data['current']['condition']['icon']}"
        st.image(icon_url)
        st.write(f"**Condition:** {condition}")
    wind_kph = weather_data['current']['wind_kph']
    wind_dir = weather_data['current']['wind_dir']
    st.write(f"**Wind:** {wind_kph} kph {wind_dir}")

# -------------------------------
# Main App
# -------------------------------

def main():
    st.title('🌤️ Weather Widget App')

    # Initialize session state for location
    if 'location_name' not in st.session_state:
        st.session_state['location_name'] = DEFAULT_LOCATION
        # Get default location coordinates
        default_location_data = get_location_suggestions(DEFAULT_LOCATION)
        if default_location_data:
            st.session_state['lat'] = default_location_data[0]['lat']
            st.session_state['lon'] = default_location_data[0]['lon']
        else:
            st.error("Unable to get default location coordinates.")
            return

    # Location Input with Autocomplete
    st.write("## Enter a location:")
    location_query = st.text_input("", value=st.session_state['location_name'], key='location_input')

    # Fetch location suggestions
    suggestions = get_location_suggestions(location_query)
    suggestion_names = [s['display_name'] for s in suggestions]

    if suggestion_names:
        # Autocomplete selection
        selected_location = st.selectbox("Select a location:", suggestion_names)
        selected_index = suggestion_names.index(selected_location)
        selected_lat = suggestions[selected_index]['lat']
        selected_lon = suggestions[selected_index]['lon']

        # Update session state
        st.session_state['location_name'] = selected_location
        st.session_state['lat'] = selected_lat
        st.session_state['lon'] = selected_lon
    else:
        st.write("No location suggestions available. Showing default location.")
        # Use default location coordinates
        st.session_state['location_name'] = DEFAULT_LOCATION

    # Get and display weather data
    weather = get_weather(st.session_state['lat'], st.session_state['lon'])
    if weather:
        display_weather_info(weather, st.session_state['location_name'])
    else:
        st.error("Unable to retrieve weather data.")

    # Additional content can be added here
    st.write("---")
    st.write("This is the rest of the app content.")

if __name__ == '__main__':
    main()
