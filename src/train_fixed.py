import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import os
import sys
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

sys.path.append('.')

from src.model import DiabetesPredictor

def load_and_prepare_data():
    """Load data and create a fitted scaler"""
    print("📂 Loading diabetes data...")
    
    # Load data
    df = pd.read_csv('data/diabetes.csv')
    
    # Handle missing values
    for col in ['Glucose', 'BloodPressure', 'BMI']:
        if col in df.columns:
            zeros = (df[col] == 0).sum()
            if zeros > 0:
                median_val = df[col][df[col] != 0].median()
                df.loc[df[col] == 0, col] = median_val
                print(f"   Replaced {zeros} zeros in {col} with median: {median_val:.1f}")
    
    # Separate features and target
    X = df.drop('Outcome', axis=1).values
    y = df['Outcome'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create and FIT the scaler on training data
    print("🔄 Fitting StandardScaler on training data...")
    scaler = StandardScaler()
    scaler.fit(X_train)  # THIS IS CRITICAL!
    
    # Transform the data
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✅ Scaler fitted! Mean shape: {scaler.mean_.shape}")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_model_fixed(epochs=100, batch_size=32, learning_rate=0.001):
    """Train model with properly fitted scaler"""
    
    # Load and prepare data
    X_train, X_test, y_train, y_test, scaler = load_and_prepare_data()
    
    # Convert to PyTorch tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test)
    
    # Create datasets
    train_dataset = torch.utils.data.TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = torch.utils.data.TensorDataset(X_test_tensor, y_test_tensor)
    
    # Create data loaders
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🚀 Using device: {device}")
    
    # Initialize model
    model = DiabetesPredictor().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Create save directory
    os.makedirs('saved_models', exist_ok=True)
    
    print("\n🏋️ Starting training...")
    print("-" * 50)
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        
        for features, labels in train_loader:
            features, labels = features.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels.view(-1, 1))
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        
        # Print every 10 epochs
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_train_loss:.4f}")
    
    print("-" * 50)
    print("✅ Training complete!")
    
    # Save model AND fitted scaler
    model_path = 'saved_models/diabetes_model_fixed.pth'
    
    # Save with both model and scaler
    torch.save({
        'model_state_dict': model.state_dict(),
        'scaler': scaler,  # This is the FITTED scaler!
        'model_architecture': 'DiabetesPredictor',
        'features': ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    }, model_path)
    
    print(f"💾 Model and fitted scaler saved to: {model_path}")
    
    # Also save scaler separately as backup
    with open('saved_models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print(f"💾 Scaler also saved separately to: saved_models/scaler.pkl")
    
    # Final evaluation
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for features, labels in test_loader:
            features, labels = features.to(device), labels.to(device)
            outputs = model(features)
            predicted = (outputs > 0.5).float()
            total += labels.size(0)
            correct += (predicted.view(-1) == labels).sum().item()
    
    accuracy = 100 * correct / total
    print(f"\n📊 Final Test Accuracy: {accuracy:.2f}%")
    
    return model, scaler

if __name__ == "__main__":
    model, scaler = train_model_fixed(epochs=100)
    
    print("\n✅ Verification:")
    print(f"   Scaler type: {type(scaler)}")
    print(f"   Scaler is fitted: {hasattr(scaler, 'n_features_in_')}")
    if hasattr(scaler, 'n_features_in_'):
        print(f"   Features expected: {scaler.n_features_in_}")
        print(f"   Mean values (first 3): {scaler.mean_[:3]}")