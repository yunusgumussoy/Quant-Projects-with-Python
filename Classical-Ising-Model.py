# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 21:49:04 2024

@author: Yunus
"""


import numpy as np
import matplotlib.pyplot as plt
from random import choice

# Parameters
L = 10  # Size of the grid (LxL)
J = 1.0  # Interaction strength (positive means neighbors prefer to align)
H = 0.0  # External field
T = 2.5  # Temperature

# Initialize a grid of spins (+1 or -1 randomly)
spins = np.random.choice([-1, 1], size=(L, L))

def energy(spins, i, j):
    """Calculate the energy of a single spin at position (i, j)"""
    total_energy = 0
    for (di, dj) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ni, nj = (i + di) % L, (j + dj) % L  # Periodic boundary conditions
        total_energy += -J * spins[i, j] * spins[ni, nj]
    total_energy -= H * spins[i, j]  # External field term
    return total_energy

def metropolis(spins, T):
    """Perform one step of the Metropolis algorithm."""
    i, j = np.random.randint(0, L, size=2)  # Pick a random spin
    dE = -2 * energy(spins, i, j)  # Change in energy if spin is flipped
    if dE < 0 or np.random.rand() < np.exp(-dE / T):
        spins[i, j] *= -1  # Flip the spin

# Simulate the Ising model
steps = 10000
for step in range(steps):
    metropolis(spins, T)

# Plot the final state
plt.imshow(spins, cmap='coolwarm')
plt.title('Final Spin Configuration (Classical Ising Model)')
plt.show()
