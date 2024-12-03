from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/app/clean', methods=['POST'])  # Add leading slash
def clean_data():
    result = subprocess.run(['python', 'app/clean_5.py'], capture_output=True, text=True)
    return jsonify({"message": "Cleaning completed", "output": result.stdout})

@app.route('/app/create-db', methods=['POST'])  # Add leading slash
def create_db():
    result = subprocess.run(['python', 'app/create_db.py'], capture_output=True, text=True)
    return jsonify({"message": "Database created", "output": result.stdout})

@app.route('/app/insert-data', methods=['POST'])  # Add leading slash
def insert_data():
    result = subprocess.run(['python', 'app/insert.py'], capture_output=True, text=True)
    return jsonify({"message": "Data inserted", "output": result.stdout})

@app.route('/app/view-data', methods=['GET'])  # Add leading slash
def view_data():
    result = subprocess.run(['python', 'app/select.py'], capture_output=True, text=True)
    return jsonify({"data": result.stdout})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment variable
    app.run(debug=True, host='0.0.0.0', port=port)  # Bind to 0.0.0.0 and use the correct port
