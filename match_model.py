# p is the probability that player A wins a point when A is serving
# q is the probability that player B wins a point when B is serving

import numpy as np
import torch
import torch.nn as nn
import json

# Load player mapping
with open('player_to_id.json', 'r') as f:
    player_to_id = json.load(f)

num_players = len(player_to_id)

# Define the model class
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
        x = torch.sigmoid(self.fc3(x))
        return x

# Load the model
model = TennisProbModel(num_players)
model.load_state_dict(torch.load('tennis_model.pth'))
model.eval()

# Ask for player names
player_a = input("Enter name of Player A: ")
player_b = input("Enter name of Player B: ")

if player_a not in player_to_id or player_b not in player_to_id:
    print("One or both players not found in training data.")
    exit()

p1_id = player_to_id[player_a]
p2_id = player_to_id[player_b]
input_tensor = torch.tensor([[p1_id, p2_id]], dtype=torch.float32)

with torch.no_grad():
    output = model(input_tensor)

p, q = output[0].tolist()
print(f"Predicted p (A wins when serving): {p:.4f}")
print(f"Predicted q (B wins when serving): {q:.4f}")

# please enable this while number of matches is small, as it will log the details of each match in a file named "game_log.txt".
logging_enabled = False
log_file = open("game_log.txt", "w")

def play_point(server,p,q):
    if server == 'A':
        if np.random.rand() < p:
            return 'A'
        else:
            return 'B'
    else:
        if np.random.rand() < q:
            return 'B'
        else:
            return 'A'

def play_game(server,p,q):
    score_a = 0
    score_b = 0
    while True:
        point_winner = play_point(server,p,q)
        if point_winner == 'A':
            score_a += 1
        else:
            score_b += 1
        log_file.write(f"\t\t\tPoint winner: {point_winner}, current score: Player A {score_a} - Player B {score_b}\n") if logging_enabled else None
        if (score_a >= 4 and score_a - score_b >= 2) or (score_b >= 4 and score_b - score_a >= 2):
            return point_winner
        if score_a == 3 and score_b == 3:
            while True:
                point_winner = play_point(server,p,q)
                if point_winner == 'A':
                    score_a += 1
                else:
                    score_b += 1
                log_file.write(f"\t\t\tPoint winner: {point_winner}, current score: Player A {score_a} - Player B {score_b}\n") if logging_enabled else None
                if (score_a >= 4 and score_a - score_b >= 2) or (score_b >= 4 and score_b - score_a >= 2):
                    return point_winner



def play_set(p,q,initial_server='A'):
    game_score_a = 0
    game_score_b = 0
    while True:
        log_file.write(f"\t\tSimulating game {game_score_a + game_score_b + 1}, current score: Player A {game_score_a} - Player B {game_score_b}\n") if logging_enabled else None
        game_winner = play_game(initial_server,p,q)
        if game_winner == 'A':
            game_score_a += 1
            log_file.write(f"\t\t\tPlayer A wins the game, current score: Player A {game_score_a} - Player B {game_score_b}\n") if logging_enabled else None
        else:
            game_score_b += 1
            log_file.write(f"\t\t\tPlayer B wins the game, current score: Player A {game_score_a} - Player B {game_score_b}\n") if logging_enabled else None

        if (game_score_a >= 6 and game_score_a - game_score_b >= 2) or (game_score_b >= 6 and game_score_b - game_score_a >= 2):
            return 'A' if game_score_a > game_score_b else 'B'
        log_file.write(f"\t\t\tCurrent game score: Player A {game_score_a} - Player B {game_score_b}\n") if logging_enabled else None
        if game_score_a == 6 and game_score_b == 6:
            log_file.write(f"\t\tSet score is 6-6, entering tiebreaker\n") if logging_enabled else None
            server = initial_server
            last_server = server
            deuce_score_a = 0
            deuce_score_b = 0
            while True:
                point_winner = play_point(server,p,q)
                if point_winner == 'A':
                    deuce_score_a += 1
                else:
                    deuce_score_b += 1
                if (deuce_score_a >= 7 and deuce_score_a - deuce_score_b >= 2) or (deuce_score_b >= 7 and deuce_score_b - deuce_score_a >= 2):
                    return 'A' if deuce_score_a > deuce_score_b else 'B'
                log_file.write(f"\t\t\tPoint winner: {point_winner}, current score: Player A {deuce_score_a} - Player B {deuce_score_b}\n") if logging_enabled else None
                if server == 'A' and last_server == 'A':
                    server = 'B'
                elif server == 'B' and last_server == 'B':
                    server = 'A'
                last_server = server

        initial_server = 'B' if initial_server == 'A' else 'A'

def simulate_matches(num_matches,number_of_sets,p,q):
    if np.random.rand() < 0.5:
        initial_server = 'A'
    else:
        initial_server = 'B'
    player_a_wins = 0
    player_b_wins = 0
    
    for match_count in range(num_matches):
        log_file.write(f"Simulating match {match_count+1}/{num_matches}\n") if logging_enabled else None
        server = initial_server
        player_a_set_wins = 0
        player_b_set_wins = 0
        if match_count % 100000 == 0:
            print(f"Simulating match {match_count+1}/{num_matches}, completed: {(match_count+1)/num_matches*100:.2f}%")
        while not (player_a_set_wins >= number_of_sets/2 or player_b_set_wins >= number_of_sets/2):
            log_file.write(f"\tSimulating set {player_a_set_wins + player_b_set_wins + 1}, current score: Player A {player_a_set_wins} - Player B {player_b_set_wins}\n") if logging_enabled else None
            set_winner = play_set(p,q,server)
            if set_winner == 'A':
                player_a_set_wins += 1
                log_file.write(f"\tPlayer A wins the set, current score: Player A {player_a_set_wins} - Player B {player_b_set_wins}\n") if logging_enabled else None
            else:
                player_b_set_wins += 1
                log_file.write(f"\tPlayer B wins the set, current score: Player A {player_a_set_wins} - Player B {player_b_set_wins}\n") if logging_enabled else None   
            server = 'B' if server == 'A' else 'A'
        if player_a_set_wins > player_b_set_wins:
            player_a_wins += 1
            log_file.write(f"Player A wins the match, current score: Player A {player_a_wins} - Player B {player_b_wins}\n") if logging_enabled else None
        else:
            player_b_wins += 1
            log_file.write(f"Player B wins the match, current score: Player A {player_a_wins} - Player B {player_b_wins}\n") if logging_enabled else None

    return player_a_wins, player_b_wins

if __name__ == "__main__":
    num_matches = 10000
    number_of_sets = 3
    player_a_wins, player_b_wins = simulate_matches(num_matches,number_of_sets,p,q)
    print(f"Player A won {player_a_wins} out of {num_matches} matches.")
    print(f"Player B won {player_b_wins} out of {num_matches} matches.")
    print(f"Estimated probability that player A wins the set: {player_a_wins/num_matches}")
    print(f"Estimated probability that player B wins the set: {player_b_wins/num_matches}")