from flask_cors import CORS
from flask import Flask, render_template

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template('tienda.html')

if __name__ == '__main__':
    app.run(debug=True)