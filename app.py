from flask import Flask, render_template, url_for, redirect, request, jsonify, session
import folium
from folium.plugins import Geocoder
import geocoder
import json

app = Flask(__name__)
app.secret_key = 'session' 

@app.route('/')
def home():
    # Create a map centered at a specific location
    map = folium.Map(
        location=[49.26218662575472, -123.24927174424609],
        titles='Stamen Terrain',
        zoom_start=12,
    )

    loc = session.get('location')
    if loc:
        lat, lon = loc[0], loc[1]
        folium.Marker([lat, lon], popup='Current Location').add_to(map)
    # else:
        # folium.Marker([49.26218662575472, -123.24927174424609], popup='Default Location').add_to(map)


    # map.add_child(folium.LatLngPopup())

    Geocoder().add_to(map)
    map.get_root().width = "900px"
    map.get_root().height = "1000px"
    
    iframe = map.get_root()._repr_html_()

    return render_template('index.html', iframe=iframe)

@app.route('/get_current_loc', methods=['POST'])
def get_current_loc():
    if request.is_json:
        data = request.get_json()
        session['location'] = data
        print(f"current location: {data[0]}, {data[1]}")
        return data
    else:
        return jsonify({'error': 'Invalid request, JSON data expected.'}), 415 
    
#     g = geocoder.ip('me')
#     return g.latlng
# loc = get_current_loc()
# print(f"current loc:{loc[0]},{loc[1]}")

# button for finding the shortest path
@app.route('/run_sim', methods=['POST'])
def run_sim():
    # add button function
    print("Button clicked")
    return redirect(url_for('home'))  # Redirect back to home after processing

if __name__ == "__main__":
    app.run(debug=True)