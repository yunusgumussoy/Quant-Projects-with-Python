# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 22:01:06 2024

@author: Yunus
"""

import numpy as np
import random
import matplotlib.pyplot as plt

# Parameters
num_agents = 101  # Number of agents (odd number to ensure a minority exists)
num_strategies_per_agent = 2  # Each agent has 2 strategies to choose from
memory_size = 3  # How many previous outcomes agents remember
num_rounds = 50  # Number of rounds in the game

# Initialize agent strategies and scores
class Agent:
    def __init__(self, memory_size):
        # Each agent gets `num_strategies_per_agent` random strategies
        self.strategies = [self.random_strategy(memory_size) for _ in range(num_strategies_per_agent)]
        self.scores = [0 for _ in range(num_strategies_per_agent)]  # Scores for strategies
        self.memory = []  # Agent's memory of previous outcomes

    def random_strategy(self, memory_size):
        """ Create a random strategy: a mapping from memory to action (buy/sell). """
        num_possible_memories = 2 ** memory_size
        return [random.choice([0, 1]) for _ in range(num_possible_memories)]

    def choose_action(self):
        """ Choose an action based on the best performing strategy. """
        if len(self.memory) < memory_size:
            # If not enough history, choose randomly
            return random.choice([0, 1])
        
        # Get the best-performing strategy
        best_strategy_idx = np.argmax(self.scores)
        best_strategy = self.strategies[best_strategy_idx]
        
        # Convert memory to an index (only if memory is large enough)
        memory_idx = int(''.join(map(str, self.memory[-memory_size:])), 2)
        return best_strategy[memory_idx]

    def update_memory(self, outcome):
        """ Update memory with the latest outcome. """
        if len(self.memory) >= memory_size:
            self.memory.pop(0)  # Keep memory within `memory_size`
        self.memory.append(outcome)

    def update_score(self, action, minority_action):
        """ Update score for strategies based on whether the agent was in the minority. """
        if len(self.memory) < memory_size:
            return  # Don't update scores if memory is not fully populated yet
        
        for i, strategy in enumerate(self.strategies):
            memory_idx = int(''.join(map(str, self.memory[-memory_size:])), 2)
            if strategy[memory_idx] == minority_action:
                self.scores[i] += 1

# Initialize agents
agents = [Agent(memory_size) for _ in range(num_agents)]

# Track global outcomes (0 = sell, 1 = buy)
history = []

def play_round():
    """ Play one round of the Minority Game. """
    actions = [agent.choose_action() for agent in agents]
    outcome = sum(actions)
    
    # Determine the minority action (0 if more buy, 1 if more sell)
    minority_action = 1 if outcome < num_agents // 2 else 0
    history.append(minority_action)
    
    # Update agent scores and memories
    for agent in agents:
        # Update memory for each agent with the current minority action
        agent.update_memory(minority_action)
        # Update score based on whether the agent was in the minority
        if len(agent.memory) >= memory_size:
            agent.update_score(agent.memory[-1], minority_action)

# Run the simulation
for round_number in range(num_rounds):
    play_round()

# Plot the outcomes
plt.plot(history, label='Minority Action (0 = Sell, 1 = Buy)')
plt.xlabel('Round')
plt.ylabel('Minority Action')
plt.title('Minority Game Outcomes Over Time')
plt.legend()
plt.show()
