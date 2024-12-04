from flask import Flask, jsonify, render_template, send_file, request
import os
from app.clean_5 import clean_csv
from app.db_create import create_database
from app.select import fetch_all_data
from app.insert import insert_data_into_db

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            print("No file part in the request.")
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename == '':
            print("No file selected for uploading.")
            return jsonify({"error": "No file selected"}), 400

        upload_path = os.path.join(app.root_path, "app", "uploads", file.filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        print(f"File uploaded successfully: {upload_path}")
        return jsonify({"message": "File uploaded successfully", "filename": file.filename})
    except Exception as e:
        print(f"Error in upload_file: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/db/create', methods=['POST'])
def db_create():
    try:
        db_path = os.path.join(app.root_path, "app", "plantilla_data.db")
        create_database(db_path)
        return jsonify({"message": "Database created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/db/select', methods=['GET'])
def db_select():
    try:
        db_path = os.path.join(app.root_path, "app", "plantilla_data.db")
        data = fetch_all_data(db_path)
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/db/insert', methods=['POST'])
def db_insert():
    try:
        db_path = os.path.join(app.root_path, "app", "plantilla_data.db")
        plantilla_path = os.path.join(app.root_path, "app", "static", "plantilla_csv.csv")
        insert_data_into_db(plantilla_path, db_path)
        return jsonify({"message": "Data inserted successfully into the database"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Registered routes:")
    print(app.url_map)  # Log all registered routes
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
