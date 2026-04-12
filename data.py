import pandas as pd
import numpy as np
data = pd.read_csv('archive/charting-m-points-to-2009.csv')
print(data.head())

players = np.array([])
for i in (data['match_id'].unique()):
    player1, player2 = i.split('-')[4:6]
    if player1 not in players:
        players = np.append(players, player1)
    if player2 not in players:
        players = np.append(players, player2)
print("Number of players:", len(players))


output_data = []
progress = 0

for i in data['match_id'].unique():
    player1, player2 = i.split('-')[4:6]
    if player1 not in players:
        players = np.append(players, player1)
    if player2 not in players:
        players = np.append(players, player2)
    progress += 1
    if progress % 10 == 0:
        print(f"Progress: {progress}/{len(data['match_id'].unique())}")
    player_1_wins_when_serving = 0
    player_1_wins_when_receiving = 0
    player_2_wins_when_serving = 0
    player_2_wins_when_receiving = 0
    for j in data[data['match_id'] == i].index:
        if data['PtWinner'][j] == data['Svr'][j]:
            if data['PtWinner'][j] == 1:
                player_1_wins_when_serving += 1
            elif data['PtWinner'][j] == 2:
                player_2_wins_when_serving += 1
        
        elif data['PtWinner'][j] != data['Svr'][j]:
            if data['PtWinner'][j] == 1:
                player_1_wins_when_receiving += 1
            elif data['PtWinner'][j] == 2:
                player_2_wins_when_receiving += 1
    r_1 = player_1_wins_when_receiving / (player_1_wins_when_receiving + player_2_wins_when_serving)
    r_2 = player_2_wins_when_receiving / (player_2_wins_when_receiving + player_1_wins_when_serving)
    s_1 = player_1_wins_when_serving / (player_1_wins_when_serving + player_2_wins_when_receiving)
    s_2 = player_2_wins_when_serving / (player_2_wins_when_serving + player_1_wins_when_receiving)
    output_data.append([player1, player2, r_1, r_2, s_1, s_2])
output_data = pd.DataFrame(output_data, columns=['Player 1', 'Player 2', 'R1', 'R2', 'S1', 'S2'])
output_data.to_csv('output_data.csv', index=False)
            
