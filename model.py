import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json

# Load the processed data
data = pd.read_csv('output_data.csv')

# Get unique players and create mapping
players = list(set(data['Player 1'].tolist() + data['Player 2'].tolist()))
player_to_id = {p: i for i, p in enumerate(players)}
id_to_player = {i: p for p, i in player_to_id.items()}

# Save player mapping
with open('player_to_id.json', 'w') as f:
    json.dump(player_to_id, f)

# Prepare training data
X = []
y = []
for _, row in data.iterrows():
    p1 = player_to_id[row['Player 1']]
    p2 = player_to_id[row['Player 2']]
    X.append([p1, p2])
    y.append([row['S1'], row['S2']])
    # Add reverse for symmetry
    X.append([p2, p1])
    y.append([row['S2'], row['S1']])

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32)

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to tensors
X_train = torch.tensor(X_train)
y_train = torch.tensor(y_train)
X_test = torch.tensor(X_test)
y_test = torch.tensor(y_test)

# Define the neural network model
class TennisProbModel(nn.Module):
    def __init__(self, num_players, embed_dim=10, hidden_dim=64):
        super(TennisProbModel, self).__init__()
        self.player_embed = nn.Embedding(num_players, embed_dim)
        self.fc1 = nn.Linear(embed_dim * 2, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, 2)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        p1_emb = self.player_embed(x[:, 0].long())
        p2_emb = self.player_embed(x[:, 1].long())
        x = torch.cat([p1_emb, p2_emb], dim=1)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout(x)
        x = torch.sigmoid(self.fc3(x))  # Output probabilities between 0 and 1
        return x

# Initialize model
num_players = len(players)
model = TennisProbModel(num_players)

# Loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
epochs = 200
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 20 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

# Save the trained model
torch.save(model.state_dict(), 'tennis_model.pth')
print("Model saved to tennis_model.pth")

# Evaluation
model.eval()
with torch.no_grad():
    test_outputs = model(X_test)
    test_loss = criterion(test_outputs, y_test)
    print(f'Test MSE Loss: {test_loss.item():.4f}')
    
    # Calculate additional metrics
    y_test_np = y_test.numpy()
    test_outputs_np = test_outputs.numpy()
    mae = mean_absolute_error(y_test_np, test_outputs_np)
    rmse = np.sqrt(mean_squared_error(y_test_np, test_outputs_np))
    print(f'Test MAE: {mae:.4f}')
    print(f'Test RMSE: {rmse:.4f}')
    
    # Calculate accuracy within certain thresholds (e.g., within 0.1 of true value)
    threshold = 0.1
    accurate_predictions = np.mean(np.abs(test_outputs_np - y_test_np) < threshold)
    print(f'Accuracy (within {threshold}): {accurate_predictions:.4f}')

# Function to predict p and q for two players
def predict_match_probabilities(player1, player2):
    """
    Predict p and q for a match between player1 and player2.
    p: probability player1 wins when serving
    q: probability player2 wins when serving
    """
    if player1 not in player_to_id or player2 not in player_to_id:
        raise ValueError("One or both players not found in training data")
    
    p1_id = player_to_id[player1]
    p2_id = player_to_id[player2]
    
    input_tensor = torch.tensor([[p1_id, p2_id]], dtype=torch.float32)
    
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
    
    p, q = output[0].tolist()
    return p, q

# Example usage
if __name__ == "__main__":
    # Example: predict for first two players in data
    sample_player1 = data['Player 1'].iloc[5]
    sample_player2 = data['Player 2'].iloc[0]
    p, q = predict_match_probabilities(sample_player1, sample_player2)
    print(f"Predicted p (P1 win when serving): {p:.4f}")
    print(f"Predicted q (P2 win when serving): {q:.4f}")