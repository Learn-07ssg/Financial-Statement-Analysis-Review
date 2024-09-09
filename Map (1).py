import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_player import st_player


# Streamlit app
def main():
    st.title("Cognizant Office ")

    # Initialize the map centered at a specific location
    m = folium.Map(location=[20, 0], zoom_start=2, title="Cognizant")  # Centered at the equator, zoom level 2

    # Cognizant's major office locations
    cognizant_offices = [
        {"location": [12.9716, 77.5946], "tooltip": "Bangalore, India"},
        {"location": [13.0827, 80.2707], "tooltip": "Chennai, India"},
        {"location": [11.0168, 76.9558], "tooltip": "Coimbatore, India"},
        {"location": [28.4595, 77.0266], "tooltip": "Gurgaon, India"},
        {"location": [17.3850, 78.4867], "tooltip": "Hyderabad, India"},
        {"location": [9.9312, 76.2673], "tooltip": "Kochi, India"},
        {"location": [22.5726, 88.3639], "tooltip": "Kolkata, India"},
        {"location": [12.9141, 74.8560], "tooltip": "Mangalore, India"},
        {"location": [19.0760, 72.8777], "tooltip": "Mumbai, India"},
        {"location": [28.5355, 77.3910], "tooltip": "Noida, India"},
        {"location": [18.5204, 73.8567], "tooltip": "Pune, India"},
        {"location": [40.7128, -74.0060], "tooltip": "New York, USA"},
        {"location": [40.8933, -74.0113], "tooltip": "Teaneck, USA"},
        {"location": [37.7749, -122.4194], "tooltip": "San Francisco, USA"},
        {"location": [32.7767, -96.7970], "tooltip": "Dallas, USA"},
        {"location": [33.4484, -112.0740], "tooltip": "Phoenix, USA"},
        {"location": [43.6532, -79.3832], "tooltip": "Toronto, Canada"},
        {"location": [45.5017, -73.5673], "tooltip": "Montreal, Canada"},
        {"location": [49.2827, -123.1207], "tooltip": "Vancouver, Canada"},
        {"location": [-23.5505, -46.6333], "tooltip": "São Paulo, Brazil"},
        {"location": [-22.9068, -43.1729], "tooltip": "Rio de Janeiro, Brazil"},
        {"location": [-34.6037, -58.3816], "tooltip": "Buenos Aires, Argentina"},
        {"location": [19.4326, -99.1332], "tooltip": "Mexico City, Mexico"},
        {"location": [9.9281, -84.0907], "tooltip": "San José, Costa Rica"},
        {"location": [13.6929, -89.2182], "tooltip": "San Salvador, El Salvador"},
        {"location": [51.5074, -0.1278], "tooltip": "London, UK"},
        {"location": [53.3498, -6.2603], "tooltip": "Dublin, Ireland"},
        {"location": [48.8566, 2.3522], "tooltip": "Paris, France"},
        {"location": [50.1109, 8.6821], "tooltip": "Frankfurt, Germany"},
        {"location": [48.1351, 11.5820], "tooltip": "Munich, Germany"},
        {"location": [45.4642, 9.1900], "tooltip": "Milan, Italy"},
        {"location": [40.4168, -3.7038], "tooltip": "Madrid, Spain"},
        {"location": [41.3851, 2.1734], "tooltip": "Barcelona, Spain"},
        {"location": [-33.8688, 151.2093], "tooltip": "Sydney, Australia"},
        {"location": [-37.8136, 144.9631], "tooltip": "Melbourne, Australia"},
        {"location": [39.9042, 116.4074], "tooltip": "Beijing, China"},
        {"location": [31.2304, 121.4737], "tooltip": "Shanghai, China"},
        {"location": [35.6895, 139.6917], "tooltip": "Tokyo, Japan"},
        {"location": [1.3521, 103.8198], "tooltip": "Singapore, Singapore"},
        {"location": [22.3193, 114.1694], "tooltip": "Hong Kong SAR, China"},
        {"location": [3.1390, 101.6869], "tooltip": "Kuala Lumpur, Malaysia"},
        {"location": [-36.8485, 174.7633], "tooltip": "Auckland, New Zealand"},
        {"location": [14.5995, 120.9842], "tooltip": "Manila, Philippines"}
    ]

    # Embed a YouTube video with autoplay
    st.markdown("""
    <iframe width="710" height="400" src="https://www.youtube.com/embed/mxF1MimxSGQ?autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """, unsafe_allow_html=True)

    # Add each location to the map
    for office in cognizant_offices:
        folium.Marker(
            location=office["location"],
            tooltip=office["tooltip"]
        ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=710, height=400)

    

if __name__ == "__main__":
    main()
