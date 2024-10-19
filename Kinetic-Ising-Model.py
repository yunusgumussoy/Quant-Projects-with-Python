# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 21:50:03 2024

@author: Yunus
"""


import numpy as np
import matplotlib.pyplot as plt

# Parameters
L = 10  # Grid size
J = 1.0  # Interaction strength
T = 2.5  # Temperature

# Initialize spins randomly
spins = np.random.choice([-1, 1], size=(L, L))

def local_energy(spins, i, j):
    """Calculate the local energy of a spin (i, j) with its neighbors."""
    total_energy = 0
    for (di, dj) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ni, nj = (i + di) % L, (j + dj) % L  # Periodic boundaries
        total_energy += -J * spins[i, j] * spins[ni, nj]
    return total_energy

def glauber_step(spins, T):
    """Perform one Glauber step."""
    i, j = np.random.randint(0, L, size=2)  # Random spin
    dE = 2 * local_energy(spins, i, j)  # Change in energy if spin is flipped
    # Flip the spin with probability based on temperature
    if np.random.rand() < 1 / (1 + np.exp(dE / T)):
        spins[i, j] *= -1  # Flip the spin

# Simulate the Kinetic Ising Model
steps = 10000
for step in range(steps):
    glauber_step(spins, T)

# Plot the final configuration
plt.imshow(spins, cmap='coolwarm')
plt.title('Final Spin Configuration (Kinetic Ising Model)')
plt.show()
