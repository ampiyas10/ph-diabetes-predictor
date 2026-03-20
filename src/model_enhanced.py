import torch
import torch.nn as nn
import torch.nn.functional as F

class EnhancedDiabetesPredictor(nn.Module):
    """
    Enhanced neural network for better diabetes prediction
    """
    
    def __init__(self, input_size=8, output_size=1):
        super(EnhancedDiabetesPredictor, self).__init__()
        
        # Deeper network with more neurons
        self.fc1 = nn.Linear(input_size, 64)
        self.bn1 = nn.BatchNorm1d(64)
        
        self.fc2 = nn.Linear(64, 32)
        self.bn2 = nn.BatchNorm1d(32)
        
        self.fc3 = nn.Linear(32, 16)
        self.bn3 = nn.BatchNorm1d(16)
        
        self.fc4 = nn.Linear(16, 8)
        self.bn4 = nn.BatchNorm1d(8)
        
        self.fc5 = nn.Linear(8, output_size)
        
        # Regularization
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        
        x = F.relu(self.bn3(self.fc3(x)))
        x = self.dropout(x)
        
        x = F.relu(self.bn4(self.fc4(x)))
        x = self.dropout(x)
        
        x = torch.sigmoid(self.fc5(x))
        return x