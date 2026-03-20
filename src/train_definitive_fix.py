import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os
import pickle
import sys
sys.path.append('.')

from src.model import DiabetesPredictor

print("=" * 50)
print("DEFINITIVE FIX: Training model with proper scaler")
print("=" * 50)

# Step 1: Load data
print("\n1️⃣ Loading data...")
df = pd.read_csv('data/diabetes.csv')
print(f"   Loaded {len(df)} samples")

# Step 2: Clean data
print("\n2️⃣ Cleaning data...")
for col in ['Glucose', 'BloodPressure', 'BMI']:
    zeros = (df[col] == 0).sum()
    if zeros > 0:
        median_val = df[col][df[col] != 0].median()
        df.loc[df[col] == 0, col] = median_val
        print(f"   Fixed {zeros} zeros in {col}")

# Step 3: Prepare features and target
X = df.drop('Outcome', axis=1).values
y = df['Outcome'].values

# Step 4: Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: CREATE AND FIT SCALER (CRITICAL STEP)
print("\n3️⃣ Creating and FITTING scaler...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Verify scaler is fitted
print(f"   ✅ Scaler is fitted! Mean shape: {scaler.mean_.shape}")
print(f"   ✅ First 3 mean values: {scaler.mean_[:3]}")
print(f"   ✅ First 3 scale values: {scaler.scale_[:3]}")

# Step 6: Convert to tensors
X_train_tensor = torch.FloatTensor(X_train_scaled)
y_train_tensor = torch.FloatTensor(y_train).view(-1, 1)
X_test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1)

# Step 7: Create model
print("\n4️⃣ Creating model...")
model = DiabetesPredictor()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Step 8: Train
print("\n5️⃣ Training model...")
epochs = 100
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"   Epoch {epoch+1}/{epochs} - Loss: {loss.item():.4f}")

# Step 9: Evaluate
print("\n6️⃣ Evaluating model...")
with torch.no_grad():
    train_preds = (model(X_train_tensor) > 0.5).float()
    train_acc = (train_preds == y_train_tensor).float().mean()
    
    test_preds = (model(X_test_tensor) > 0.5).float()
    test_acc = (test_preds == y_test_tensor).float().mean()
    
    print(f"   ✅ Training accuracy: {train_acc.item()*100:.2f}%")
    print(f"   ✅ Test accuracy: {test_acc.item()*100:.2f}%")

# Step 10: SAVE BOTH MODEL AND SCALER (CRITICAL STEP)
print("\n7️⃣ Saving model and scaler...")
os.makedirs('saved_models', exist_ok=True)

# Save as one file
torch.save({
    'model_state_dict': model.state_dict(),
    'scaler': scaler,
    'test_accuracy': test_acc.item(),
    'train_accuracy': train_acc.item()
}, 'saved_models/diabetes_model_fixed.pth')
print(f"   ✅ Saved to: saved_models/diabetes_model_fixed.pth")

# Also save scaler separately as backup
with open('saved_models/scaler_fixed.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print(f"   ✅ Scaler backup saved to: saved_models/scaler_fixed.pkl")

# Step 11: VERIFY THE SAVED FILE
print("\n8️⃣ Verifying saved file...")
check = torch.load('saved_models/diabetes_model_fixed.pth', map_location='cpu')
print(f"   ✅ File contains: {list(check.keys())}")
if 'scaler' in check:
    print(f"   ✅ Scaler is in the file!")
    print(f"   ✅ Scaler mean (first 3): {check['scaler'].mean_[:3]}")
else:
    print(f"   ❌ Scaler NOT found in file!")

print("\n" + "=" * 50)
print("✅ DEFINITIVE FIX COMPLETE!")
print("=" * 50)