from flask import Flask, render_template, url_for, redirect, request, jsonify, session
import folium
from folium.plugins import Geocoder
import geocoder
import json

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
        
        user_loc = folium.ClickForMarker("<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}")

        map.add_child(
            user_loc   
        )      

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
                    background-color: #f9fafb'>
                    Set as Start Point
                </button>
            </div>
        """, script=True)


        popup = folium.Popup(popup_html, max_width=500)

        folium.Marker([lat, lon], popup=popup).add_to(map)

        # map.add_child(folium.LatLngPopup())

        Geocoder().add_to(map)
        map.get_root().width = "900px"
        map.get_root().height = "1000px"
        
        iframe = map.get_root()._repr_html_()

        start_loc = session['start_location']

    return render_template('index.html', iframe=iframe, start_loc=start_loc)

@app.route('/get_current_loc', methods=['POST'])
def get_current_loc():
    if request.is_json:
        data = request.get_json()
        session['location'] = data
        print(f"current location: {data[0]}, {data[1]}")
        return data
    else:
        return jsonify({'error': 'Invalid request, JSON data expected.'}), 415 

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
    # add button function
    print("Button clicked")
    return redirect(url_for('home'))  # Redirect back to home after processing

def add_wildfire_layer(map):
    # TODO: Link to actual wildfire data
    wildfire_coordinates = [
        {
            "latitude": 49.26970086788797, 
            "longitude": -123.25513912793387
        },
        {
            "latitude": 49.26610568647218, 
            "longitude": -123.2369701635495
        }
    ]

    wildfire_layer = folium.FeatureGroup(name="Wildfire Locations")
    for coordinate in wildfire_coordinates:
        # print(f"Latitude: {coordinate['latitude']}, Longitude: {coordinate['longitude']}")
        wildfire_layer.add_child(folium.Marker(
            location=[coordinate['latitude'], coordinate['longitude']],
            popup="Wildfire",
            icon=folium.Icon(icon='fire', color='red', prefix='fa')
        ))

    map.add_child(wildfire_layer)

def custom_code(popup_variable_name, map_variable_name, folium_port):
    return '''
            // custom code
            function latLngPop(e) {
                %s
                    .setLatLng(e.latlng)
                    .setContent(`
                        lat: ${e.latlng.lat}, lng: ${e.latlng.lng}
                        <button onClick="
                            fetch('http://localhost:%s', {
                                method: 'POST',
                                mode: 'no-cors',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    latitude: ${e.latlng.lat},
                                    longitude: ${e.latlng.lng}
                                })
                            });

                            L.marker(
                                [${e.latlng.lat}, ${e.latlng.lng}],
                                {}
                            ).addTo(%s);
                        "> Store Coordinate </button>
                        <button onClick="
                            fetch('http://localhost:%s', {
                                method: 'POST',
                                mode: 'no-cors',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: 'q'
                            });
                        "> Quit </button>
                    `)
                    .openOn(%s);
            }
            // end custom code
    ''' % (popup_variable_name, folium_port, map_variable_name, folium_port, map_variable_name)

if __name__ == "__main__":
    app.run(debug=True)