from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Load the model if it exists
MODEL_PATH = "sign_model.pkl"
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
else:
    print("Warning: sign_model.pkl not found. Prediction endpoint will be disabled.")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    data = request.json
    landmarks = data.get('landmarks') # Expecting list of 42 values
    
    if not landmarks or len(landmarks) < 42:
        return jsonify({"error": "Need 42 values (21 landmarks * 2 coords)"}), 400
    
    # Normalize: Shift all landmarks relative to the wrist (landmarks[0], landmarks[1])
    base_x, base_y = landmarks[0], landmarks[1]
    norm_landmarks = []
    for i in range(0, 42, 2):
        norm_landmarks.append(landmarks[i] - base_x)
        norm_landmarks.append(landmarks[i+1] - base_y)
    
    prediction = model.predict([norm_landmarks])
    return jsonify({"prediction": str(prediction[0])})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "Backend is running", "model_loaded": model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
