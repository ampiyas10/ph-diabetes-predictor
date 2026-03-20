import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
import sys
sys.path.append('.')

from src.model import DiabetesPredictor
from src.data_loader import prepare_data

def calculate_metrics(y_true, y_pred):
    """Calculate classification metrics"""
    y_true = y_true.numpy()
    y_pred = y_pred.numpy()
    
    accuracy = (y_true == y_pred).mean()
    
    # Confusion matrix
    tp = ((y_true == 1) & (y_pred == 1)).sum()
    tn = ((y_true == 0) & (y_pred == 0)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    return {
        'accuracy': accuracy,
        'sensitivity': sensitivity,
        'specificity': specificity,
        'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn
    }

def train_model(epochs=300, batch_size=32, learning_rate=0.001):
    """
    Train the diabetes prediction model
    """
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🚀 Using device: {device}")
    
    # Load data
    train_loader, test_loader, scaler = prepare_data(batch_size=batch_size)
    
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
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels.view(-1, 1))
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        
        # Print every 10 epochs
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_train_loss:.4f}")
    
    print("-" * 50)
    print("✅ Training complete!")
    
    # Save the model
    model_path = 'saved_models/diabetes_model.pth'
    torch.save({
        'model_state_dict': model.state_dict(),
        'scaler': scaler,
    }, model_path)
    print(f"💾 Model saved to: {model_path}")
    
    # Final evaluation
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for features, labels in test_loader:
            features = features.to(device)
            outputs = model(features)
            predicted = (outputs.cpu() > 0.5).float()
            all_preds.append(predicted)
            all_labels.append(labels)
    
    all_preds = torch.cat(all_preds)
    all_labels = torch.cat(all_labels)
    metrics = calculate_metrics(all_labels, all_preds)
    
    print("\n📊 Final Model Performance:")
    print(f"   Accuracy: {metrics['accuracy']:.2%}")
    print(f"   Sensitivity (detects diabetes): {metrics['sensitivity']:.2%}")
    print(f"   Specificity: {metrics['specificity']:.2%}")
    print(f"\n   Confusion Matrix:")
    print(f"      True Positives:  {metrics['tp']}")
    print(f"      True Negatives:  {metrics['tn']}")
    print(f"      False Positives: {metrics['fp']}")
    print(f"      False Negatives: {metrics['fn']}")
    
    return model, scaler

if __name__ == "__main__":
    model, scaler = train_model()