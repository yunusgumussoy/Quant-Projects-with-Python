# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 22:12:38 2024

@author: Yunus
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_spins = 100  # Number of spins in the system
temperature = 2.0  # Temperature (higher means more random behavior)
num_steps = 100  # Number of simulation steps

# Initialize spins randomly (+1 or -1)
spins = np.random.choice([-1, 1], size=num_spins)

# Function to compute the average magnetization
def magnetization(spins):
    return np.mean(spins)

# Mean-field interaction step
magnetizations = []
for step in range(num_steps):
    # Calculate the mean field (average magnetization)
    mean_field = magnetization(spins)
    
    # Each spin interacts with the mean field and updates
    for i in range(num_spins):
        local_field = mean_field  # In mean-field, local field is just the average
        prob = 1 / (1 + np.exp(-2 * local_field / temperature))  # Boltzmann probability
        spins[i] = 1 if np.random.rand() < prob else -1
    
    # Record the magnetization
    magnetizations.append(magnetization(spins))

# Plot the magnetization over time
plt.plot(magnetizations)
plt.title('Magnetization in a Mean-Field Ising Model')
plt.xlabel('Step')
plt.ylabel('Magnetization')
plt.show()
