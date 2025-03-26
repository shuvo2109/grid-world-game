import json
import random

class Environment:
    def __init__(self, size, mode='debug'):
        self.width = size[0]
        self.height = size[1]

        self.states = [(x, y) for x in range(self.width) for y in range(self.height)]

        self.mode = mode

        self.green_cells = []
        self.red_cells = []
        self.obstacles = []

        self.p1_position = (0, 0)
        self.p2_position = (0, 0)

        self.assign_obstacles()
        self.assign_players()

        print(f"Environment generated.")

    def assign_obstacles(self, green_density=3/36, red_density=2/36, obstacle_density=8/36):
        if self.mode.lower() == "debug":
            self.green_cells = [(4, 0), (1, 3)]
            self.red_cells = [(0, 0), (4, 1), (1, 5)]
            self.obstacles = [(3, 0), (3, 1), (0, 2), (1, 2), (4, 3), (5, 3), (2, 4), (2, 5)]

        else:
            available_positions = list(self.states)

            # Green Cells
            num_green = int(self.width * self.height * green_density)
            self.green_cells = random.sample(available_positions, num_green)

            # Red Cells
            available_positions = [pos for pos in available_positions if pos not in self.green_cells]
            num_red = int(self.width * self.height * red_density)
            self.red_cells = random.sample(available_positions, num_red)

            # Obstacles
            available_positions = [pos for pos in available_positions if pos not in self.red_cells]
            num_obstacles = int(self.width * self.height * obstacle_density)
            self.obstacles = random.sample(available_positions, num_obstacles)

    def assign_players(self):
        if self.mode == "debug":
            self.p1_position = (2, 2)
            self.p2_position = (3, 3)
        else:
            occupied_positions = set(self.obstacles + self.red_cells + self.green_cells)
            available_positions = [pos for pos in self.states if pos not in occupied_positions]

            # Player 1 position
            self.p1_position = random.choice(available_positions)

            # Player 2 position
            available_positions.remove(self.p1_position)
            self.p2_position = random.choice(available_positions)

    def save_to_json(self, filename="environment.json"):
        env_data = {
            "p1_position": self.p1_position,
            "p2_position": self.p2_position,
            "obstacles": self.obstacles,
            "red_cells": self.red_cells,
            "green_cells": self.green_cells
        }

        with open(filename, "w") as f:
            json.dump(env_data, f, indent=2)

        print(f"Environment saved to {filename}.")

    def is_valid(self, pos):
        return (0 <= pos[0] < self.width and 0 <= pos[1] < self.height and pos not in self.obstacles)

    def move(self, pos, action):
        moves = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        move_offset = moves.get(action, (0, 0))  # Default to (0,0) for any other action
        new_pos = (pos[0] + move_offset[0], pos[1] + move_offset[1])

        return new_pos if self.is_valid(new_pos) else pos


def neighbors(pos):
    x, y = pos

    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

