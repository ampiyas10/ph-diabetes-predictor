import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
import sys
sys.path.append('.')

from src.model_enhanced import EnhancedDiabetesPredictor
from src.data_loader import prepare_data

def train_enhanced_model(epochs=300, batch_size=32, learning_rate=0.001):
    """
    Train enhanced model with better architecture
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🚀 Using device: {device}")
    
    train_loader, test_loader, scaler = prepare_data(batch_size=batch_size)
    
    # Use enhanced model
    model = EnhancedDiabetesPredictor().to(device)
    criterion = nn.BCELoss()
    
    # Better optimizer with weight decay
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=20)
    
    os.makedirs('saved_models', exist_ok=True)
    
    print("\n🏋️ Training enhanced model...")
    print("-" * 50)
    
    best_accuracy = 0
    
    for epoch in range(epochs):
        # Training
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
        scheduler.step(avg_train_loss)
        
        # Validation every 10 epochs
        if (epoch + 1) % 10 == 0:
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
            print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_train_loss:.4f} - Val Accuracy: {accuracy:.2f}%")
            
            # Save best model
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                torch.save({
                    'model_state_dict': model.state_dict(),
                    'scaler': scaler,
                    'accuracy': accuracy
                }, 'saved_models/best_model.pth')
    
    print("-" * 50)
    print(f"✅ Training complete! Best accuracy: {best_accuracy:.2f}%")
    print(f"💾 Best model saved to: saved_models/best_model.pth")
    
    return model, scaler

if __name__ == "__main__":
    model, scaler = train_enhanced_model()