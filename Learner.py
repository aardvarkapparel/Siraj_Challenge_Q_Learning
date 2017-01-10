__author__ = 'philippe'
import World
import threading
import time
import math

discount = 0.5
#discount = -0.6
actions = World.actions
states = []
Q = {}

# Make a list of tuples for the board size
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

# For each tuple in the list of states, make a dictionary for each action (up/down/left/right)
# and assign an intial value of 0.1 and draw the little triangles for each direction
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

# for all the specials (green/red squares), set the value to the special value (-1, or +1)
for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2


def max_Q(s):
    val = None
    act = None;
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    while True:
        # Pick the right action
        s = World.player
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)

        #increase the discount as learning progresses to accelerate convergence
        #discount += 0.1

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            t = 1.0
            # reset discount rate
            #discount += -0.06

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.05)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()