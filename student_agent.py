# Remember to adjust your student ID in meta.xml
import numpy as np
import pickle
import random
import gym
from simple_custom_taxi_env import SimpleTaxiEnv


def get_action(obs):
    
    # TODO: Train your own agent
    # HINT: If you're using a Q-table, consider designing a custom key based on `obs` to store useful information.
    # NOTE: Keep in mind that your Q-table may not cover all possible states in the testing environment.
    #       To prevent crashes, implement a fallback strategy for missing keys. 
    #       Otherwise, even if your agent performs well in training, it may fail during testing.

    # read q_table
    with open('q_table.pkl', 'rb') as f:
        q_table = pickle.load(f)
    # get state
    taxi_row, taxi_col, _,_,_,_,_,_,_,_,obstacle_north, obstacle_south, obstacle_east, obstacle_west, passenger_look, destination_look = obs
    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west)
    if state not in q_table:
        return random.choice([0, 1, 2, 3, 4, 5])
    action = np.argmax(q_table[state])
    return action
    # You can submit this random agent to evaluate the performance of a purely random strategy.