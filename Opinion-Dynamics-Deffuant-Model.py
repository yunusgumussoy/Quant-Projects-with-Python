# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 22:13:09 2024

@author: Yunus
"""

import numpy as np
import random
import matplotlib.pyplot as plt

# Parameters
num_agents = 100  # Number of agents
num_rounds = 200  # Number of interaction rounds
convergence_rate = 0.5  # How quickly opinions converge during an interaction
threshold = 0.2  # Maximum opinion difference to allow interaction

# Initialize random opinions between 0 and 1
opinions = np.random.rand(num_agents)

# Function to simulate one round of the Deffuant model
def simulate_round(opinions):
    for _ in range(num_agents):
        # Randomly choose two agents to interact
        agent1, agent2 = random.sample(range(num_agents), 2)
        
        # Check if their opinions are close enough to interact
        if abs(opinions[agent1] - opinions[agent2]) < threshold:
            # Update opinions based on the convergence rate
            new_opinion1 = opinions[agent1] + convergence_rate * (opinions[agent2] - opinions[agent1])
            new_opinion2 = opinions[agent2] + convergence_rate * (opinions[agent1] - opinions[agent2])
            opinions[agent1], opinions[agent2] = new_opinion1, new_opinion2

# Simulate the opinion dynamics
opinions_over_time = []
for _ in range(num_rounds):
    simulate_round(opinions)
    opinions_over_time.append(opinions.copy())

# Plot the evolution of opinions
plt.plot(opinions_over_time)
plt.title('Opinion Dynamics in Deffuant Model')
plt.xlabel('Round')
plt.ylabel('Opinions')
plt.show()
