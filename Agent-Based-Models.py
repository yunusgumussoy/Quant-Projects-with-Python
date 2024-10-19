# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 21:52:27 2024

@author: Yunus
"""

# pip install Mesa

from mesa import Agent, Model
from mesa.time import RandomActivation
import random

class TraderAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = random.choice(["buy", "sell"])

    def step(self):
        # Agents can copy the behavior of their neighbors
        neighbors = self.model.schedule.agents
        if neighbors:
            self.state = random.choice([agent.state for agent in neighbors])

class MarketModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            agent = TraderAgent(i, self)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()

# Simulate the model
model = MarketModel(100)
for i in range(100):  # Run for 100 steps
    model.step()

# Print the final states of the agents
final_states = [agent.state for agent in model.schedule.agents]
print(f"Final states: {final_states}")
