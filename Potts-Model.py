# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 22:14:21 2024

@author: Yunus
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
L = 10  # Lattice size (L x L grid)
T = 2.5  # Temperature
q = 3  # Number of possible states (3 for 3-state Potts model)
num_steps = 10000  # Number of simulation steps

# Initialize the lattice randomly with states 0, 1, or 2
lattice = np.random.randint(0, q, size=(L, L))

# Function to calculate the energy of a spin
def energy(lattice, i, j):
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    energy = 0
    for ni, nj in neighbors:
        if 0 <= ni < L and 0 <= nj < L:  # Check boundaries
            if lattice[i, j] != lattice[ni, nj]:
                energy += 1  # Energy is high if neighbors are in different states
    return energy

# Metropolis-Hastings Monte Carlo step
def metropolis_step(lattice, T):
    for _ in range(L * L):
        i, j = np.random.randint(0, L, size=2)  # Pick a random site
        current_energy = energy(lattice, i, j)
        new_state = np.random.randint(0, q)  # Propose a new state
        old_state = lattice[i, j]
        lattice[i, j] = new_state
        new_energy = energy(lattice, i, j)
        
        # Metropolis criterion: accept the new state with probability exp(-ΔE / T)
        delta_energy = new_energy - current_energy
        if delta_energy > 0 and np.random.rand() >= np.exp(-delta_energy / T):
            lattice[i, j] = old_state  # Reject the new state

# Simulate the Potts model
for step in range(num_steps):
    metropolis_step(lattice, T)

# Plot the final configuration of the lattice
plt.imshow(lattice, cmap='cool', interpolation='none')
plt.title(f'3-State Potts Model (T = {T})')
plt.colorbar(label='State')
plt.show()
