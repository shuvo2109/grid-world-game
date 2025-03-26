from environment import Environment
from players import QLearner
import json

env = Environment(size=(6, 6), mode='debug')
env.save_to_json()

A1 = ['0', 'N', 'E', 'W', 'S', 'Z']
A2 = ['0', 'N', 'E', 'W', 'S']

player1 = QLearner(actions=A1, env=env)
player2 = QLearner(actions=A2, env=env)

num_episodes = 1000
T = 10

B = 0.5
C = 0.5

trajectory = {}

for e in range(num_episodes):
    player1.position = env.p1_position
    player2.position = env.p2_position
    player2.assign_type()

    history = {
        's': [(player1.position, player2.position)],
        'a': []
    }

    trajectory[e] = {}

    for t in range(T):
        # Current State
        st = history['s'][-1]

        p1t = st[0]
        p2t = st[1]

        # Choose action
        a1t = player1.choose_action(state=st)
        a2t = player2.choose_action(state=st)

        at = (a1t, a2t)

        # Transition
        p1t_new = env.move(p1t, a1t)
        p2t_new = env.move(p2t, a2t)

        # Rewards
        r1, r2 = 0, 0

        if a1t == 'Z' and player2.type == 0:
            r1, r2 = -C, -C

            s_new = 'sink'

            player1.Q_update(s=st, a=a1t, r=r1, s_new=s_new)
            player2.Q_update(s=st, a=a2t, r=r2, s_new=s_new)

            history['s'].append(s_new)
            history['a'].append(at)

            break


        if player2.type == 0 and p2t_new in env.green_cells:
            r1, r2 = 1, 1

        if player2.type == 1 and p2t_new in env.red_cells:
            r1, r2 = -B, B

        s_new = (p1t_new, p2t_new)

        # Q-update
        player1.Q_update(s=st, a=a1t, r=r1, s_new=s_new)
        player2.Q_update(s=st, a=a2t, r=r2, s_new=s_new)

        p1Q = player1.Q
        p2Q = player2.Q

        history['s'].append(s_new)
        history['a'].append(at)

        trajectory[e][t] = {
            "p1t": p1t,
            "p2t": p2t,
            "a1t": a1t,
            "a2t": a2t,
            "r1": r1,
            "r2": r2,
            "p1Q": player1.Q[st][a1t],
            "p2Q": player2.Q[st][a2t]
        }


    if e % 100 == 0:
        print(f"Simulation done for Episode {e}.")

with open("trajectory.json", "w") as f:
    json.dump(trajectory, f, indent=4)

print("Game simulation complete. Trajectory saved to trajectory.json.")
