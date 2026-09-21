from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
import random

#Mesa Implementation
class UserAgent(Agent):
    """Represents a simulated user."""
    def __init__(self, unique_id, model, is_authorized):
        super().__init__(unique_id, model)
        self.is_authorized = is_authorized
        self.authenticated = False

    def step(self):
        """Simulates an attempt to authenticate."""
        if self.is_authorized:
            self.authenticated = random.random() > 0.1  # 90% success
        else:
            self.authenticated = random.random() > 0.7  # 30% success

        # Update model's stats
        if self.authenticated:
            self.model.success_count += 1
        else:
            self.model.failure_count += 1

class SecuritySystemModel(Model):
    """Represents the security system."""
    def __init__(self, num_users, width, height):
        self.num_users = num_users
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.success_count = 0
        self.failure_count = 0

        # Create agents
        for i in range(self.num_users):
            is_authorized = random.choice([True, False])
            user = UserAgent(i, self, is_authorized)
            self.schedule.add(user)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(user, (x, y))

        self.datacollector = DataCollector(
            {"Successes": lambda m: m.success_count,
             "Failures": lambda m: m.failure_count}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

def agent_portrayal(agent):
    """Visualize agents in Mesa."""
    if agent.is_authorized:
        portrayal = {"Shape": "circle", "Color": "green", "r": 0.5, "Layer": 1}
    else:
        portrayal = {"Shape": "circle", "Color": "red", "r": 0.5, "Layer": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = ChartModule([
    {"Label": "Successes", "Color": "green"},
    {"Label": "Failures", "Color": "red"}
])

server = ModularServer(
    SecuritySystemModel,
    [grid, chart],
    "Security System Simulation",
    {"num_users": 20, "width": 10, "height": 10}
)
