from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', name="Wild-Fire-Mapping")

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