# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 22:02:56 2024

@author: Yunus
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
N = 100  # Total number of individuals
p = 0.01  # Independent switching probability
h = 0.1  # Herding strength
num_steps = 200  # Number of simulation steps

# Initial state: Half in State A, half in State B
num_in_A = N // 2  # Number of individuals in state A
num_in_B = N - num_in_A  # Number of individuals in state B

# Store the fraction of individuals in each state over time
history_A = []
history_B = []

def switch(num_in_A, num_in_B):
    """ Simulate one time step of switching between states. """
    # Calculate the probabilities of switching
    # From A to B
    p_A_to_B = p + h * (num_in_B / N)
    # From B to A
    p_B_to_A = p + h * (num_in_A / N)

    # Number of individuals switching from A to B
    num_switch_A_to_B = np.random.binomial(num_in_A, p_A_to_B)
    # Number of individuals switching from B to A
    num_switch_B_to_A = np.random.binomial(num_in_B, p_B_to_A)

    # Update the number of individuals in each state
    num_in_A_new = num_in_A + num_switch_B_to_A - num_switch_A_to_B
    num_in_B_new = N - num_in_A_new

    return num_in_A_new, num_in_B_new

# Run the simulation
for step in range(num_steps):
    history_A.append(num_in_A / N)  # Track the fraction in state A
    history_B.append(num_in_B / N)  # Track the fraction in state B
    
    # Update the states based on switching probabilities
    num_in_A, num_in_B = switch(num_in_A, num_in_B)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(history_A, label='Fraction in State A (Bullish)')
plt.plot(history_B, label='Fraction in State B (Bearish)')
plt.xlabel('Time Step')
plt.ylabel('Fraction of Population')
plt.title("Kirman's Ant Colony Model: Fraction of Bullish vs. Bearish Traders Over Time")
plt.legend()
plt.grid(True)
plt.show()
