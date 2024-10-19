# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 21:57:55 2024

@author: Yunus
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
grid_size = 20  # Size of the grid (20x20)
p_influence = 0.5  # Probability of being influenced by neighbors to sell
num_steps = 15  # Number of simulation steps
initial_sell_fraction = 0.05  # Fraction of agents that start by selling

# Initialize grid with '0' for holding and '1' for selling
grid = np.zeros((grid_size, grid_size), dtype=int)

# Randomly initialize some agents as sellers
num_initial_sellers = int(initial_sell_fraction * grid_size**2)
initial_sellers = random.sample([(i, j) for i in range(grid_size) for j in range(grid_size)], num_initial_sellers)

for (i, j) in initial_sellers:
    grid[i, j] = 1  # Set to '1' (sell)

def plot_grid(grid, step):
    """ Function to visualize the grid. """
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='coolwarm', interpolation='nearest')
    plt.title(f'Step {step}')
    plt.colorbar(label='0 = Hold, 1 = Sell')
    plt.show()

def get_neighbors(i, j, grid_size):
    """ Return the list of neighbors for an agent at position (i, j). """
    neighbors = []
    if i > 0: neighbors.append((i-1, j))  # Up
    if i < grid_size - 1: neighbors.append((i+1, j))  # Down
    if j > 0: neighbors.append((i, j-1))  # Left
    if j < grid_size - 1: neighbors.append((i, j+1))  # Right
    return neighbors

def percolation_step(grid, p_influence, grid_size):
    """ Perform one step of the percolation process. """
    new_grid = grid.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == 0:  # Only consider agents currently holding
                neighbors = get_neighbors(i, j, grid_size)
                # Count the proportion of neighbors that are selling
                sell_count = sum([grid[n_i, n_j] for n_i, n_j in neighbors])
                if sell_count > 0 and random.random() < p_influence:
                    new_grid[i, j] = 1  # This agent decides to sell
    return new_grid

# Simulate and visualize the percolation process
for step in range(num_steps):
    plot_grid(grid, step)
    grid = percolation_step(grid, p_influence, grid_size)
