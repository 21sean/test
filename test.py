# Default location set to China
DEFAULT_LOCATION = 'China'

# -------------------------------
# Helper Functions
# -------------------------------

def get_location_suggestions(query):
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
                'name': name,
                'region': region,
                'country': country,
                'lat': lat,
                'lon': lon
            })
    return suggestions

def get_weather(lat, lon):
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={lat},{lon}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_news(country_name):
    country_code = country_name_to_code(country_name)
    if not country_code:
        return []
    url = f'https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={NEWSAPI_KEY}&pageSize=5'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return articles
    return []

def country_name_to_code(country_name):
    import pycountry
    try:
        country = pycountry.countries.get(name=country_name)
        if not country:
            country = pycountry.countries.search_fuzzy(country_name)[0]
        return country.alpha_2.lower()
    except:
        return None

# -------------------------------
# Main App
# -------------------------------

def main():
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
            .css-18e3th9 {
                padding-top: 0rem;
            }
            .css-1d391kg {
                padding-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title('🌤️ Weather and News Widget App')
    
    if 'location_name' not in st.session_state:
        st.session_state['location_name'] = DEFAULT_LOCATION
        default_location_data = get_location_suggestions(DEFAULT_LOCATION)
        if default_location_data:
            st.session_state['lat'] = default_location_data[0]['lat']
            st.session_state['lon'] = default_location_data[0]['lon']
            st.session_state['country'] = default_location_data[0]['country']
        else:
            st.error("Unable to get default location coordinates.")
            return

    st.write("## Enter a location:")
    location_query = st.text_input("", value=st.session_state['location_name'], key='location_input')

    suggestions = get_location_suggestions(location_query)
    suggestion_names = [s['display_name'] for s in suggestions]

    if suggestion_names:
        selected_location = st.selectbox("Select a location:", suggestion_names)
        selected_index = suggestion_names.index(selected_location)
        selected_lat = suggestions[selected_index]['lat']
        selected_lon = suggestions[selected_index]['lon']
        selected_country = suggestions[selected_index]['country']
        st.session_state['location_name'] = selected_location
        st.session_state['lat'] = selected_lat
        st.session_state['lon'] = selected_lon
        st.session_state['country'] = selected_country
    else:
        st.write("No location suggestions available. Showing default location.")
        st.session_state['location_name'] = DEFAULT_LOCATION

    weather = get_weather(st.session_state['lat'], st.session_state['lon'])
    articles = get_news(st.session_state.get('country', ''))

    with elements("dashboard"):
        layout = [
            dashboard.Item("weather_widget", 0, 0, 6, 4),
            dashboard.Item("news_widget", 6, 0, 6, 8),
        ]
        with dashboard.Grid(layout, draggableHandle=".draggable"):
            with mui.Paper(key="weather_widget", elevation=3, sx={"padding": "16px"}):
                mui.Typography("Weather", variant="h6", className="draggable")
                if weather:
                    temp_c = weather['current']['temp_c']
                    feelslike_c = weather['current']['feelslike_c']
                    humidity = weather['current']['humidity']
                    condition = weather['current']['condition']['text']
                    icon_url = f"http:{weather['current']['condition']['icon']}"
                    wind_kph = weather['current']['wind_kph']
                    wind_dir = weather['current']['wind_dir']

                    mui.Box(
                        mui.Typography(f"Temperature: {temp_c} °C (Feels like {feelslike_c} °C)"),
                        mui.Typography(f"Humidity: {humidity}%"),
                        mui.Typography(f"Condition: {condition}"),
                        mui.Typography(f"Wind: {wind_kph} kph {wind_dir}"),
                        mui.Avatar(src=icon_url, variant="square", sx={"width": 64, "height": 64}),
                    )
                else:
                    mui.Typography("Unable to retrieve weather data.")

            with mui.Paper(key="news_widget", elevation=3, sx={"padding": "16px"}):
                mui.Typography("Latest News Headlines", variant="h6", className="draggable")
                if articles:
                    for article in articles:
                        title = article.get('title')
                        description = article.get('description')
                        url = article.get('url')
                        urlToImage = article.get('urlToImage')
                        publishedAt = article.get('publishedAt')
                        source = article.get('source', {}).get('name')

                        with mui.Card(sx={"marginBottom": "15px"}):
                            if urlToImage:
                                mui.CardMedia(
                                    component="img",
                                    image=urlToImage,
                                    height="140",
                                )
                            with mui.CardContent:
                                mui.Typography(title, gutterBottom=True, variant="h6", component="div")
                                mui.Typography(f"{publishedAt[:10]} | {source}", color="text.secondary", variant="body2")
                                mui.Typography(description, variant="body2", color="text.secondary")
                            mui.CardActions(
                                mui.Button("Read More", href=url, target="_blank")
                            )
                else:
                    mui.Typography("No news articles available for this location.")

    st.write("---")
    st.write("This is the rest of the app content.")

if __name__ == '__main__':
    main()
