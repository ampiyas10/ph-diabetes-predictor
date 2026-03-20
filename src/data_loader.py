import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DiabetesDataset(Dataset):
    """Custom Dataset class for diabetes data"""
    
    def __init__(self, features, labels):
        self.features = torch.FloatTensor(features)
        self.labels = torch.FloatTensor(labels)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

def prepare_data(batch_size=32, test_size=0.2):
    """
    Load and prepare diabetes data for PyTorch
    """
    print("📂 Loading diabetes data...")
    
    # Load data
    df = pd.read_csv('data/diabetes.csv')
    
    # Handle missing values (replace 0 with median for certain columns)
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
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✅ Data prepared:")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    print(f"   Features: {X.shape[1]}")
    
    # Create datasets
    train_dataset = DiabetesDataset(X_train_scaled, y_train)
    test_dataset = DiabetesDataset(X_test_scaled, y_test)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, test_loader, scaler

# Test the data loader
if __name__ == "__main__":
    train_loader, test_loader, scaler = prepare_data()
    
    # Check a batch
    features, labels = next(iter(train_loader))
    print(f"\n📦 Sample batch:")
    print(f"   Features shape: {features.shape}")
    print(f"   Labels shape: {labels.shape}")
    print(f"   Sample features: {features[0][:5]}...")
    print(f"   Sample label: {labels[0]}")