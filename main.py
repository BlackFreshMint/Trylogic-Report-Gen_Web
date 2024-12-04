from flask import Flask, jsonify, render_template, send_file, request
import os
from app.clean_5 import clean_csv
from app.db_create import create_database
from app.select import fetch_all_data
from app.insert import insert_data_into_db
from app.clean_db import clean_database

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Ensure the 'file' part is in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        # Ensure the user selected a file
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Validate file extension
        if not file.filename.lower().endswith('.csv'):
            return jsonify({"error": "Only CSV files are allowed"}), 400

        # Save the uploaded file to the uploads folder
        upload_path = os.path.join(app.root_path, "app", "uploads", file.filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        # Path for the cleaned file
        output_path = os.path.join(app.root_path, "app", "output", "cleaned_data_exam.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Path to the template CSV
        plantilla_path = os.path.join(app.root_path, "app", "static", "plantilla_csv.csv")

        # Clean the uploaded CSV
        clean_csv(upload_path, output_path, plantilla_path)

        # Notify success
        return jsonify({"message": f"File uploaded and cleaned successfully: {file.filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download_cleaned_file():
    try:
        output_path = os.path.join(app.root_path, "app", "output", "cleaned_data_exam.csv")
        return send_file(output_path, as_attachment=True)
    except Exception as e:
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

@app.route('/db/clean', methods=['POST'])
def db_clean():
    try:
        db_path = os.path.join(app.root_path, "app", "plantilla_data.db")
        clean_database(db_path)
        return jsonify({"message": "Database cleaned successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Registered routes:")
    print(app.url_map)  # Log all registered routes
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
