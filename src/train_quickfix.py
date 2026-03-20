import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import sys
sys.path.append('.')

from src.model import DiabetesPredictor

# Load data
df = pd.read_csv('data/diabetes.csv')
print(f"📊 Loaded {len(df)} samples")

# Handle missing values
for col in ['Glucose', 'BloodPressure', 'BMI']:
    df[col] = df[col].replace(0, df[col].median())

# Prepare data
X = df.drop('Outcome', axis=1).values
y = df['Outcome'].values

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and fit scaler (THIS IS THE KEY!)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to tensors
X_train = torch.FloatTensor(X_train)
y_train = torch.FloatTensor(y_train).view(-1, 1)
X_test = torch.FloatTensor(X_test)
y_test = torch.FloatTensor(y_test).view(-1, 1)

# Create model
model = DiabetesPredictor()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train
print("Training...")
for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/100 - Loss: {loss.item():.4f}")

# Test
with torch.no_grad():
    predictions = model(X_test)
    accuracy = ((predictions > 0.5).float() == y_test).float().mean()
    print(f"✅ Accuracy: {accuracy.item()*100:.2f}%")

# Save model AND scaler
os.makedirs('saved_models', exist_ok=True)
torch.save({
    'model_state_dict': model.state_dict(),
    'scaler': scaler,
}, 'saved_models/diabetes_model_fixed.pth')

print("✅ Model and fitted scaler saved to saved_models/diabetes_model_fixed.pth")