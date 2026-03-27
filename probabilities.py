# p = probability that player A wins a point when A is serving
# 1-p = probability that player B wins a point when A is serving
# q = probability that player B wins a point when B is serving
# 1-q = probability that player A wins a point when B is serving

import matplotlib.pyplot as plt
import numpy as np

def game_win_probab(x):
    return x**4 + 4*(1-x)*x**4 + 10*(1-x)**2*x**4 + 20*(1-x)**3*x**5/((1-2*x*(1-x)))

def set_win_probab(p,q):
    t = game_win_probab(p)
    r = 1-game_win_probab(q)
    score_7_6_probab = p*(1-q)/(1-(p*q + (1-p)*(1-q)))
    return (
        t**3*r**3 #6-0
        + 3*(1-t)*t**3*r**3 + 3*(1-r)*t**4*r**2 # 6-1
        + 6*(1-t)**2*t**2*r**4 + 12*(1-t)*(1-r)*t**3*r**3 + 3*(1-r)**2*t**4*r**2 # 6-2  
        + 4*(1-t)**3*t**2*r**4 + 24*(1-t)**2*(1-r)*t**3*r**3 + 24*(1-t)*(1-r)**2*t**4*r**2 + 4*(1-r)**3*t**5*r # 6-3
        + 5*(1-t)**4*t*r**5 + 40*(1-t)**3*(1-r)*t**2*r**4 + 60*(1-t)**2*(1-r)**2*t**3*r**3 + 20*(1-t)*(1-r)**3*t**4*r**2 + (1-r)**4*t**5*r # 6-4
        + r*t*(
            (1-t)**5*r**5 + 25*(1-t)**4*(1-r)*t*r**4 + 100*(1-t)**3*(1-r)**2*t**2*r**3 + 100*(1-t)**2*(1-r)**3*t**3*r**2 + 25*(1-t)*(1-r)**4*t**4*r + (1-r)**5*t**5
        ) # 7-5
        + ((t*(1-r)+r*(1-t))*(
            (1-t)**5*r**5 + 25*(1-t)**4*(1-r)*t*r**4 + 100*(1-t)**3*(1-r)**2*t**2*r**3 + 100*(1-t)**2*(1-r)**3*t**3*r**2 + 25*(1-t)*(1-r)**4*t**4*r + (1-r)**5*t**5
        )*score_7_6_probab) # 7-6
    )

# player_a_win_when_serving = float(input("Enter the probability that player A wins a point when A is serving: "))
# player_b_win_when_serving = float(input("Enter the probability that player B wins a point when B is serving: "))
# if(player_a_win_when_serving < 0 or player_a_win_when_serving > 1 or player_b_win_when_serving < 0 or player_b_win_when_serving > 1 or (player_a_win_when_serving == 0 and player_b_win_when_serving == 0) or (player_a_win_when_serving == 1 and player_b_win_when_serving == 1)):
#     print("Invalid input. Please enter a probability between 0 and 1.")
# else:
#     print(f"Probability that player A wins the set: {set_win_probab(player_a_win_when_serving, player_b_win_when_serving)}")

fig = plt.figure()
fig.suptitle('Probability that player A wins the set', fontsize=16)
fig.set_size_inches(10, 7)
ax = plt.axes(projection='3d')
p_values = [i/100 for i in range(1,100)]
q_values = [i/100 for i in range(1,100)]
P, Q = np.meshgrid(p_values, q_values)
Z = set_win_probab(P, Q)
ax.plot_surface(P, Q, Z, cmap='plasma')
ax.set_xlabel('Probability that player A wins a point when A is serving')
ax.set_ylabel('Probability that player B wins a point when B is serving')
ax.set_zlabel('Probability that player A wins the set')
# ax.elev = 90
# ax.azim = 0
surf = ax.plot_surface(P, Q, Z, cmap='plasma')
fig.colorbar(surf, ax=ax)
plt.savefig('tennis_set_win_probability.png')
plt.show()
