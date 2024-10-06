from flask import Flask, render_template, url_for, redirect, request
import folium

app = Flask(__name__)

@app.route('/')
def home():
    # Create a map centered at a specific location
    map = folium.Map(
        location=[49.26218662575472, -123.24927174424609],
        titles='Stamen Terrain',
        zoom_start=12,
    )
    map.get_root().width = "1000px"
    map.get_root().height = "400px"
    iframe = map.get_root()._repr_html_()

    # # Save the map to an HTML file
    # map_path = 'static/map.html'
    # m.save(map_path)

    return render_template('index.html', map_file='map.html', iframe=iframe)

# button for finding the shortest path
@app.route('/run_sim', methods=['POST'])
def run_sim():
    # add button function
    print("Button clicked")
    return redirect(url_for('home'))  # Redirect back to home after processing

# button for finding the shortest path
@app.route('/search',methods=['POST'])
def search():
    # add button function
    search_term = request.form.get('search_term')
    print(f"Search term: {search_term}")
    
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)