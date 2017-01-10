__author__ = 'philippe'
from tkinter import *
import random
master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 50
(x, y) = (20, 9)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (x-10, y-1)
score = 1
restart = False
walk_reward = -0.04

walls_s = [(1, 1), (1,2),  (1,3),  (1,5),  (2,1),  (2,3),  (2,4),  (2,5)]
walls_i = [(4,3),  (4,4),  (4,5)]
walls_r = [(6,2),  (6,3),  (6,4),  (6,5),  (7,2),  (8,2)]
walls_a = [(10,4), (10,5), (11,2), (11,3), (13,2), (13,3), (14,4), (14,5)]
walls_j = [(16,3), (16,7), (17,3), (17,4), (17,5), (17,6), (17,7), (18,3)]
walls_s.extend(walls_i)
walls_s.extend(walls_r)
walls_s.extend(walls_a)
walls_s.extend(walls_j)
walls = walls_s 

specials = [(12, 1, "red", -1), (4, 1, "green", 1)]
cell_scores = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)

def render_grid():
    global specials, walls, Width, x, y, player, wall_ids
    wall_ids = [] 
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        # Create a random blue color
        #r = lambda: random.randint(0,255)
        #my_color = '#0000%02X' % (r())
        tmp_id = board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)
        #print(tmp_id)
        wall_ids.append(tmp_id)
    return wall_ids
  
wall_ids = []
wall_ids = render_grid()
#render_grid()
#print("Length of wall_ids" , len(wall_ids))

def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)

        # Create a random color, normally 0-255, but elimiate the darkeest and lightest colors a bit using 25-225
        r = lambda: random.randint(25,225)
        rand_color = '#%02X%02X%02X' % (r(),r(),r())
        #board.itemconfigure(me,fill=rand_color)
        # Now re-draw the walls in the new color
        for my_id in wall_ids:
           board.itemconfigure(my_id,fill=rand_color)
           #board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=rand_color, width=1)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
                print ("Success! score: ", score)
            else:
                print ("Fail! score: ", score)
            restart = True
            return
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = (x-10, y-1)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
dth=0.5