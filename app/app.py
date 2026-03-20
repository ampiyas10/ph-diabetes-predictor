from flask import Flask, render_template, request, jsonify
import torch
import numpy as np
import os
import sys
from sklearn.preprocessing import StandardScaler
import torch.serialization
sys.path.append('.')

from src.model import DiabetesPredictor

app = Flask(__name__)

# Add CORS for production
from flask_cors import CORS
CORS(app)

# Secure loading of the model
torch.serialization.add_safe_globals([StandardScaler])

# Get the absolute path to the model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'saved_models', 'diabetes_model.pth')

# Load the trained model
device = torch.device('cpu')
model = DiabetesPredictor().to(device)
model.eval()

try:
    # Load the saved model
    if os.path.exists(MODEL_PATH):
        checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=True)
        model.load_state_dict(checkpoint['model_state_dict'])
        scaler = checkpoint['scaler']
        print(f"✅ Model loaded successfully from {MODEL_PATH}")
    else:
        print(f"❌ Model not found at {MODEL_PATH}")
        # Create a dummy scaler as fallback
        scaler = StandardScaler()
        import pandas as pd
        df = pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'diabetes.csv'))
        X = df.drop('Outcome', axis=1).values
        scaler.fit(X)
        print("⚠️ Using fallback scaler")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    scaler = StandardScaler()

feature_names = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
]

@app.route('/')
def index():
    return render_template('index.html', features=feature_names)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        features = []
        for feature in feature_names:
            value = float(request.form[feature])
            features.append(value)
        
        # Scale features
        features_scaled = scaler.transform([features])
        input_tensor = torch.FloatTensor(features_scaled)
        
        # Make prediction
        with torch.no_grad():
            probability = model(input_tensor).item()
        
        # Determine risk with Philippine context
        if probability >= 0.7:
            risk = "Mataas na Panganib (High Risk)"
            color = "#ce1126"  # Philippine red
            advice = "📞 Kumonsulta agad sa doktor. Please consult a doctor immediately."
        elif probability >= 0.4:
            risk = "Katamtamang Panganib (Moderate Risk)"
            color = "#fedc00"  # Philippine yellow
            advice = "🏥 Magpa-check up at baguhin ang lifestyle. Schedule a check-up and consider lifestyle changes."
        else:
            risk = "Mababang Panganib (Low Risk)"
            color = "#0038a8"  # Philippine blue
            advice = "💪 Panatilihin ang malusog na pamumuhay. Maintain a healthy lifestyle."
        
        return render_template('result.html',
                             probability=probability * 100,
                             risk=risk,
                             color=color,
                             advice=advice,
                             features=dict(zip(feature_names, features)))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        features = []
        for feature in feature_names:
            features.append(float(data[feature]))
        
        features_scaled = scaler.transform([features])
        input_tensor = torch.FloatTensor(features_scaled)
        
        with torch.no_grad():
            probability = model(input_tensor).item()
        
        return jsonify({
            'probability': probability,
            'risk': 'High' if probability >= 0.5 else 'Low',
            'features': dict(zip(feature_names, features)),
            'app': 'Philippine Diabetes Risk Predictor',
            'trademark': 'Ampiyas'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'app': 'Ampiyas Ⓣ'})

@app.route('/about')
def about():
    return jsonify({
        'app_name': 'Philippine Diabetes Risk Predictor',
        'trademark': 'Ampiyas',
        'version': '1.0.0',
        'description': 'AI-powered diabetes risk assessment tool for Filipinos',
        'features': feature_names
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)