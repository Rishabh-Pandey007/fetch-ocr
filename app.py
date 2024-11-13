# app.py
from flask import Flask, request, jsonify
from utils import extract_text_from_image
import os
from config import API_KEY

app = Flask(__name__)

@app.route('/extract_number', methods=['POST'])
def extract_vehicle_number():
    if 'API_KEY' not in request.headers or request.headers['API_KEY'] != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    image_path = os.path.join("temp_image.jpg")
    image.save(image_path)
    
    try:
        vehicle_number = extract_text_from_image(image_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(image_path)

    return jsonify({"vehicle_number": vehicle_number})

if __name__ == '__main__':
    app.run(debug=True)
