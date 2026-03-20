import torch
import torch.nn as nn
import torch.nn.functional as F

class DiabetesPredictor(nn.Module):
    """
    Neural network for diabetes prediction
    Input: 8 features -> Output: 1 (diabetes probability)
    """
    
    def __init__(self, input_size=8, hidden_sizes=[16, 8], output_size=1, dropout_rate=0.3):
        super(DiabetesPredictor, self).__init__()
        
        # First hidden layer
        self.fc1 = nn.Linear(input_size, hidden_sizes[0])
        self.bn1 = nn.BatchNorm1d(hidden_sizes[0])
        
        # Second hidden layer
        self.fc2 = nn.Linear(hidden_sizes[0], hidden_sizes[1])
        self.bn2 = nn.BatchNorm1d(hidden_sizes[1])
        
        # Output layer
        self.fc3 = nn.Linear(hidden_sizes[1], output_size)
        
        # Regularization
        self.dropout = nn.Dropout(dropout_rate)
        
        # Feature names for reference
        self.feature_names = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]
        
    def forward(self, x):
        # First layer
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout(x)
        
        # Second layer
        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout(x)
        
        # Output layer with sigmoid
        x = torch.sigmoid(self.fc3(x))
        
        return x
    
    def predict_proba(self, x):
        """Return probability scores"""
        self.eval()
        with torch.no_grad():
            return self.forward(x).numpy()
    
    def predict(self, x, threshold=0.5):
        """Return binary predictions"""
        probs = self.predict_proba(x)
        return (probs >= threshold).astype(int)

# Test the model
if __name__ == "__main__":
    model = DiabetesPredictor()
    print("✅ Model created:")
    print(model)
    
    # Test forward pass
    test_input = torch.randn(5, 8)  # Batch of 5 samples
    output = model(test_input)
    print(f"\n📊 Test forward pass:")
    print(f"   Input shape: {test_input.shape}")
    print(f"   Output shape: {output.shape}")
    print(f"   Sample predictions: {output[:3].detach().numpy().flatten()}")