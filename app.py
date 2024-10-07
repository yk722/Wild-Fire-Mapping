from flask import Flask, render_template, url_for, redirect, request, jsonify, session
import folium
from folium.plugins import Geocoder
import geocoder
import json
import csv
from folium.elements import MacroElement
from jinja2 import Template

"""
Overiding folium LatLngPopup to customize the popup content.
"""
class LatLngPopup(MacroElement):
    """
    When one clicks on a Map that contains a LatLngPopup,
    a popup is shown that displays the latitude and longitude of the pointer.
    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = L.popup();
            function latLngPop(e) {
                var lat = e.latlng.lat.toFixed(4);
                var lon = e.latlng.lng.toFixed(4);

                {{this.get_name()}}
                    .setLatLng(e.latlng)
                    .setContent(`
                        <button onclick="fetch('/set_start_point', {
                            method: 'POST',
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                latitude: ${lat},
                                longitude: ${lon}
                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            console.log('Result:', result.message);
                         
                            //update location on sidebar
                            document.getElementById('startLocation').innerText = ${lat} + ', ' + ${lon};
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });"
                        style='font-family: "Lato", sans-serif;
                            font-size: medium;
                            border-radius: 30px;
                            border: none;
                            color: #2e90fa;
                            background-color: #e4e7ec;'>
                            Set as Start Point
                        </button>`
                    )
                    .openOn({{this._parent.get_name()}});
            }
            {{this._parent.get_name()}}.on('click', latLngPop);
        {% endmacro %}
    """)

    def __init__(self):
        super(LatLngPopup, self).__init__()
        self._name = 'LatLngPopup'


app = Flask(__name__)
app.secret_key = 'session' 

@app.route('/')
def home():
    loc = session.get('location')

    if loc:
        lat, lon = loc[0], loc[1]

        map = folium.Map(
            location=[lat, lon],
            # titles='Stamen Terrain',
            zoom_start=12,
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
        )

        add_wildfire_layer(map)
    
        # Getting the user current location
        # and let the user to use it as the start posisition
        popup_html = folium.Html(f"""
            <div style='font-family: "Lato", sans-serif;'>
                <h4>Current Location</h4>
                <button onclick="
                    fetch('/set_start_point', {{
                        method: 'POST',
                        headers: {{
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{
                            latitude: {lat},
                            longitude: {lon}
                        }})
                    }})
                    .then(response => response.json())
                    .then(result => {{
                        console.log('Result:', result.message);
                    }})
                    .catch(error => {{
                        console.error('Error:', error);
                    }});
                "
                style='font-family: "Lato", sans-serif;
                    font-size: medium;
                    border-radius: 30px;
                    border: none;
                    color: #2e90fa;
                    background-color: #e4e7ec'>
                    Set as Start Point
                </button>
            </div>
        """, script=True)

        # Displying the popup pin on the map
        popup = folium.Popup(popup_html, max_width=500)

        folium.Marker([lat, lon], popup=popup).add_to(map)

        map.add_child(LatLngPopup())

        Geocoder().add_to(map)

        map.get_root().width = "900px"
        map.get_root().height = "1000px"
        
        iframe = map.get_root()._repr_html_()

        start_loc = session['start_location']

    return render_template('index.html', iframe=iframe, start_loc=start_loc)

# Getting user's current location
@app.route('/get_current_loc', methods=['POST'])
def get_current_loc():
    if request.is_json:
        data = request.get_json()
        session['location'] = data
        print(f"current location: {data[0]}, {data[1]}")
        return data
    else:
        return jsonify({'error': 'Invalid request, JSON data expected.'}), 415 

# Setting the start point
@app.route('/set_start_point', methods=['POST'])
def set_start_point():
    if request.is_json:
        data = request.get_json()
        lat = data.get('latitude')
        lon = data.get('longitude')

        session['start_location'] = [lat, lon]
        print(f"start location: {lat}, {lon}")

        return data
    else:
        return jsonify({'error': 'Invalid request, JSON data expected.'}), 415 

# button for finding the shortest path
@app.route('/run_sim', methods=['POST'])
def run_sim():
    # TODO: need to add proper button function
    print("Button clicked")
    return redirect(url_for('home'))  

"""
Fetch wildfire data from a csv file.

Outputs:
    - wildfire_coordinates: an array containing coordinates with latitude and longitude.
"""
def fetch_wildfire_data():
    with open('csvFiles/AnyConv.com__MODIS_C6_1_Canada_24h.csv', mode='r') as file:
        reader = csv.DictReader(file)
        wildfire_coordinates = []

        for line in reader:    
            # print(line['LATITUDE,N,32,10'])
            # print(line['LONGITUDE,N,32,10'])
            wildfire_coordinates.append({
                "latitude": line['LATITUDE,N,32,10'], 
                "longitude": line['LONGITUDE,N,32,10']
            })

        return wildfire_coordinates

"""
Add markers for wildfire on the map.
"""
def add_wildfire_layer(map):
    wildfire_coordinates = fetch_wildfire_data()

    wildfire_layer = folium.FeatureGroup(name="Wildfire Locations")
    for coordinate in wildfire_coordinates:
        # print(f"Latitude: {coordinate['latitude']}, Longitude: {coordinate['longitude']}")
        wildfire_layer.add_child(folium.Marker(
            location=[coordinate['latitude'], coordinate['longitude']],
            popup="Wildfire",
            icon=folium.Icon(icon='fire', color='red', prefix='fa')
        ))

    map.add_child(wildfire_layer)

if __name__ == "__main__":
    app.run(debug=True)