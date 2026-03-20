import torch
import sys

print("🔍 Checking your saved model file...")
try:
    checkpoint = torch.load('saved_models/diabetes_model.pth', map_location='cpu', weights_only=False)
    print("✅ File loaded successfully!")
    print(f"   Keys in checkpoint: {list(checkpoint.keys())}")
    
    if 'scaler' in checkpoint:
        print("✅ Scaler found in checkpoint!")
        scaler = checkpoint['scaler']
        
        # Check if scaler is fitted
        import sklearn
        if hasattr(scaler, 'n_features_in_'):
            print(f"✅ Scaler is fitted! (expects {scaler.n_features_in_} features)")
        else:
            print("❌ Scaler is NOT fitted!")
            
            # Check what's in the scaler
            print(f"   Scaler type: {type(scaler)}")
            print(f"   Scaler attributes: {dir(scaler)}")
    else:
        print("❌ No scaler found in checkpoint!")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n💡 Recommendation: Let's retrain with proper scaler saving!")