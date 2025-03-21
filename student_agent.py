# Remember to adjust your student ID in meta.xml
import numpy as np
import pickle
import random
import gym
import globals

def get_action(obs):
    
    # TODO: Train your own agent
    # HINT: If you're using a Q-table, consider designing a custom key based on `obs` to store useful information.
    # NOTE: Keep in mind that your Q-table may not cover all possible states in the testing environment.
    #       To prevent crashes, implement a fallback strategy for missing keys. 
    #       Otherwise, even if your agent performs well in training, it may fail during testing.

    epsilon = 0.1
    if random.uniform(0, 1) < epsilon:
        return random.choice([0, 1, 2, 3, 4, 5])

    # read q_table
    with open('q_table.pkl', 'rb') as f:
        q_table = pickle.load(f)
    # get state
    taxi_row, taxi_col, R_x, R_y, G_x, G_y, Y_x, Y_y, B_x, B_y, obstacle_north, obstacle_south, obstacle_east, obstacle_west, passenger_look, destination_look = obs
    stations = [(R_x, R_y), (G_x, G_y), (Y_x, Y_y), (B_x, B_y)]
    progress = globals.progress
    goal = stations[progress]
    if goal == (taxi_row, taxi_col):
        progress = (progress + 1) % 4
        goal = stations[progress]
        globals.progress = progress
    relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
    action = np.argmax(q_table[state])
        
    return action
    # You can submit this random agent to evaluate the performance of a purely random strategy.