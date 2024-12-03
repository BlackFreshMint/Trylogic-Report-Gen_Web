from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('app/clean', methods=['POST'])
def clean_data():
    # Call the clean_3.py script
    result = subprocess.run(['python', 'app/clean_5.py'], capture_output=True, text=True)
    return jsonify({"message": "Cleaning completed", "output": result.stdout})

@app.route('app/create-db', methods=['POST'])
def create_db():
    result = subprocess.run(['python', 'app/create_db.py'], capture_output=True, text=True)
    return jsonify({"message": "Database created", "output": result.stdout})

@app.route('app/insert-data', methods=['POST'])
def insert_data():
    result = subprocess.run(['python', 'app/insert.py'], capture_output=True, text=True)
    return jsonify({"message": "Data inserted", "output": result.stdout})

@app.route('app/view-data', methods=['GET'])
def view_data():
    result = subprocess.run(['python', 'app/select.py'], capture_output=True, text=True)
    return jsonify({"data": result.stdout})

if __name__ == '__main__':
    app.run(debug=True)
