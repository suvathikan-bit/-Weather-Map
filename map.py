import streamlit as st
from streamlit_folium import st_folium
import folium
import requests

st.set_page_config(page_title="Suvathikan Weather Map", page_icon="⛅", layout="wide")

# ---------------- Settings Panel ----------------
with st.sidebar:
    st.image("logo.png", width=120)
    st.markdown("### Settings ⚙️")
    map_layer = st.selectbox("Map Layer", ["OpenStreetMap", "CartoDB Positron", "Stamen Terrain", "Stamen Toner"])
    temp_unit = st.selectbox("Temperature Unit", ["Celsius (°C)", "Fahrenheit (°F)"])
    show_logo = st.checkbox("Show Logo", True)
    st.markdown("---")
    st.markdown("**Contact Info**")
    st.markdown("📞 +94 771236642  \n📧 suvathikan2013119@gmail.com")

if not show_logo:
    st.sidebar.empty()

# ---------------- Map ----------------
# Center map
m = folium.Map(location=[7.8731, 80.7718], zoom_start=5, tiles=None)

# Map layer selection
if map_layer == "OpenStreetMap":
    folium.TileLayer("OpenStreetMap").add_to(m)
elif map_layer == "CartoDB Positron":
    folium.TileLayer("CartoDB positron").add_to(m)
elif map_layer == "Stamen Terrain":
    folium.TileLayer("Stamen Terrain").add_to(m)
elif map_layer == "Stamen Toner":
    folium.TileLayer("Stamen Toner").add_to(m)

# Add click-to-get-weather function
st.markdown("### Click on the map to get weather info 📍")

# Use st_folium to render the map
map_data = st_folium(m, width=800, height=600)

# ---------------- Weather Fetch ----------------
API_KEY = "3729667eb86355595d2be48f76ccc8b0"

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # Unit conversion
    units = "metric" if temp_unit.startswith("C") else "imperial"

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"

    try:
        response = requests.get(url)
        data = response.json()

        city_name = data.get("name", "Unknown")
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        clouds = data["clouds"]["all"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        condition = data["weather"][0]["description"]

        st.markdown(f"### Weather Info: {city_name}")
        st.markdown(f"🌡 **Temperature:** {temp}°{'C' if units=='metric' else 'F'}")
        st.markdown(f"🤒 **Feels Like:** {feels}°{'C' if units=='metric' else 'F'}")
        st.markdown(f"🌥 **Clouds:** {clouds}%")
        st.markdown(f"💧 **Humidity:** {humidity}%")
        st.markdown(f"🌬 **Wind Speed:** {wind} m/s")
        st.markdown(f"🌈 **Condition:** {condition.title()}")

    except Exception as e:
        st.error("Error fetching weather data. Please try again.")

