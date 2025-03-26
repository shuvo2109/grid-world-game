from environment import Environment
import random

class QLearner:
    def __init__(self, actions, env: Environment, player_type=0, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.actions = actions

        self.type = player_type

        all_states = [(p1, p2) for p1 in env.states for p2 in env.states] + ['sink']

        self.Q = {s: {a: 0 for a in self.actions} for s in all_states}

        self.alpha = alpha  # Learning Rate
        self.epsilon = epsilon  # Epsilon Greedy Rate
        self.gamma = gamma  # Discount Factor

        self.position = (0, 0)

    def assign_type(self, type_0_probability=0.5):
        if random.uniform(0, 1) < type_0_probability:
            self.type = 0
        else:
            self.type = 1

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)

        q_values = self.Q[state]
        return max(q_values, key=q_values.get)

    def Q_update(self, s, a, r, s_new):
        max_next_Q = max(self.Q[s_new][a2] for a2 in self.actions)  # Max future Q-value

        # Q-learning update
        self.Q[s][a] += self.alpha * (r + self.gamma * max_next_Q - self.Q[s][a])
