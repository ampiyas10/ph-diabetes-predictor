from flask import Flask, render_template, request, jsonify
import torch
import numpy as np
import os
import sys
from sklearn.preprocessing import StandardScaler
import torch.serialization
sys.path.append('.')

from src.model import DiabetesPredictor

app = Flask(__name__, template_folder='templates')

# Add CORS for production
from flask_cors import CORS
CORS(app)

# Secure loading of the model
torch.serialization.add_safe_globals([StandardScaler])

# Get the absolute path to the model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'saved_models', 'diabetes_model_fixed.pth')

# Load the trained model
device = torch.device('cpu')
model = DiabetesPredictor().to(device)
model.eval()

print("=" * 50)
print("🚀 Starting Philippine Diabetes Risk Predictor")
print("=" * 50)

try:
    # Load the new fixed model
    if os.path.exists(MODEL_PATH):
        checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        scaler = checkpoint['scaler']  # This will now work!
        
        print(f"✅ Model loaded successfully from: {MODEL_PATH}")
        print(f"✅ Scaler is fitted! Mean values (first 3): {scaler.mean_[:3]}")
        print(f"✅ Scaler scale values (first 3): {scaler.scale_[:3]}")
        
        # Test accuracy if available
        if 'test_accuracy' in checkpoint:
            print(f"✅ Model test accuracy: {checkpoint['test_accuracy']*100:.2f}%")
    else:
        print(f"❌ Model not found at {MODEL_PATH}")
        print("⚠️ Please run: python src/train_definitive_fix.py")
        # Create a dummy scaler as fallback
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        import pandas as pd
        df = pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'diabetes.csv'))
        X = df.drop('Outcome', axis=1).values
        scaler.fit(X)
        print("⚠️ Using fallback scaler")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    # Create a dummy scaler as fallback
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    import pandas as pd
    df = pd.read_csv(os.path.join(BASE_DIR, '..', 'data', 'diabetes.csv'))
    X = df.drop('Outcome', axis=1).values
    scaler.fit(X)
    print("✅ Created and fitted fallback scaler")

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
        print("\n📝 Form data received:")
        
        # Get form data with better error handling
        features = []
        for feature in feature_names:
            # Get value from form
            value = request.form.get(feature)
            print(f"   {feature}: {value}")
            
            if value is None or value == '':
                return jsonify({'error': f'Missing value for {feature}'}), 400
            
            # Convert to float
            try:
                float_value = float(value)
                features.append(float_value)
            except ValueError:
                return jsonify({'error': f'Invalid number for {feature}: {value}'}), 400
        
        print(f"✅ Features collected: {features}")
        
        # Convert to numpy array and reshape for scaler
        import numpy as np
        features_array = np.array(features).reshape(1, -1)
        print(f"✅ Array shape: {features_array.shape}")
        
        # Scale features
        try:
            features_scaled = scaler.transform(features_array)
            print(f"✅ Features scaled successfully")
            print(f"   Scaled values (first 3): {features_scaled[0][:3]}")
        except Exception as e:
            print(f"❌ Scaler error: {e}")
            return jsonify({'error': f'Scaler error: {str(e)}'}), 400
        
        # Convert to tensor
        input_tensor = torch.FloatTensor(features_scaled)
        
        # Make prediction
        with torch.no_grad():
            probability = model(input_tensor).item()
        
        print(f"✅ Prediction: {probability:.4f} ({probability*100:.1f}%)")
        
        # Determine risk with Philippine context
        if probability >= 0.7:
            risk = "Mataas na Panganib (High Risk)"
            color = "#ce1126"  # Philippine red
            advice = "📞 Kumonsulta agad sa doktor. Please consult a doctor immediately."
            bg_color = "#ffebee"
        elif probability >= 0.4:
            risk = "Katamtamang Panganib (Moderate Risk)"
            color = "#fedc00"  # Philippine yellow
            advice = "🏥 Magpa-check up at baguhin ang lifestyle. Schedule a check-up and consider lifestyle changes."
            bg_color = "#fff8e1"
        else:
            risk = "Mababang Panganib (Low Risk)"
            color = "#0038a8"  # Philippine blue
            advice = "💪 Panatilihin ang malusog na pamumuhay. Maintain a healthy lifestyle."
            bg_color = "#e8f0fe"
        
        return render_template('result.html',
                             probability=probability * 100,
                             risk=risk,
                             color=color,
                             bg_color=bg_color,
                             advice=advice,
                             features=dict(zip(feature_names, features)))
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        features = []
        for feature in feature_names:
            features.append(float(data[feature]))
        
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        input_tensor = torch.FloatTensor(features_scaled)
        
        with torch.no_grad():
            probability = model(input_tensor).item()
        
        return jsonify({
            'probability': probability,
            'risk': 'High' if probability >= 0.5 else 'Low',
            'features': dict(zip(feature_names, features)),
            'app': 'Philippine Diabetes Risk Predictor',
            'trademark': 'Ampiyas Ⓣ'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'app': 'Philippine Diabetes Risk Predictor',
        'trademark': 'Ampiyas Ⓣ'
    })

@app.route('/about')
def about():
    return jsonify({
        'app_name': 'Philippine Diabetes Risk Predictor',
        'trademark': 'Ampiyas Ⓣ',
        'version': '1.0.0',
        'description': 'AI-powered diabetes risk assessment tool for Filipinos',
        'features': feature_names,
        'creator': 'Ampiyas'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🌐 Server running at: http://127.0.0.1:{port}")
    print("📱 Press CTRL+C to stop\n")
    app.run(host='0.0.0.0', port=port, debug=True)