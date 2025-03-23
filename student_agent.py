# Remember to adjust your student ID in meta.xml
import numpy as np
import pickle
import random
import gym
from simple_custom_taxi_env import SimpleTaxiEnv
from tqdm import tqdm
import globals

def find_nearest_station(taxi_pos, station):
    distance = np.inf
    for (x,y) in station:
        temp_distance = abs(taxi_pos[0] - x) + abs(taxi_pos[1] - y)
        if temp_distance < distance:
            distance = temp_distance
            goal = (x, y)
    return goal

def get_action(obs):
    
    # TODO: Train your own agent
    # HINT: If you're using a Q-table, consider designing a custom key based on `obs` to store useful information.
    # NOTE: Keep in mind that your Q-table may not cover all possible states in the testing environment.
    #       To prevent crashes, implement a fallback strategy for missing keys. 
    #       Otherwise, even if your agent performs well in training, it may fail during testing.

    taxi_row, taxi_col, R_x, R_y, G_x, G_y, Y_x, Y_y, B_x, B_y, obstacle_north, obstacle_south, obstacle_east, obstacle_west, passenger_look, destination_look = obs
    if globals.goal is None:
        station = [(R_x, R_y), (G_x, G_y), (Y_x, Y_y), (B_x, B_y)]
        goal = find_nearest_station((taxi_row, taxi_col), station)
        globals.goal = goal
        globals.possible_passenger = set(station)
        globals.possible_destination = set(station)
        globals.has_passenger = False
        taxi_pos = (taxi_row, taxi_col)
        relative_goal_pos = (goal[0] - taxi_pos[0], goal[1] - taxi_pos[1])
        state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
    else:
        taxi_row, taxi_col, _,_,_,_,_,_,_,_,obstacle_north, obstacle_south, obstacle_east, obstacle_west, passenger_look, destination_look = obs

        taxi_pos = (taxi_row, taxi_col)
        prev_taxi_pos = globals.prev_taxi_pos

        adjacent = set([(taxi_row + 1, taxi_col), (taxi_row - 1, taxi_col), (taxi_row, taxi_col + 1), (taxi_row, taxi_col - 1), (taxi_row, taxi_col)])

        if passenger_look:
            globals.possible_passenger.intersection_update(adjacent)
        else:
            globals.possible_passenger.difference_update(adjacent)

        if destination_look:
            globals.possible_destination.intersection_update(adjacent)
        else:
            globals.possible_destination.difference_update(adjacent)

        if globals.has_passenger == False:
            if len(globals.possible_passenger) == 1:
                if prev_taxi_pos in globals.possible_passenger and globals.prev_action == 4:
                    globals.has_passenger = True
                    globals.possible_passenger = set()
                    goal = list(globals.possible_destination)[0]
                    globals.goal = goal
                    relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
                    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
                else:
                    goal = list(globals.possible_passenger)[0]
                    globals.goal = goal
                    relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
                    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
            elif len(globals.possible_passenger) == 0:
                goal = find_nearest_station(taxi_pos, list(globals.possible_destination))
                globals.goal = goal
                relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
                state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
            else:
                if globals.goal in globals.possible_passenger:
                    goal = globals.goal
                    relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
                    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
                else:
                    goal = find_nearest_station(taxi_pos, list(globals.possible_passenger))
                    globals.goal = goal
                    relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
                    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])

        else: # has_passenger == True
            if globals.prev_action == 5:
                globals.has_passenger = False
                globals.possible_passenger = {taxi_pos}
                goal = taxi_pos
                globals.goal = goal
                relative_goal_pos = (0, 0)
                state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
            else:
                if globals.goal in globals.possible_destination:
                    goal = globals.goal
                    relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
                    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
                else:
                    goal = find_nearest_station(taxi_pos, list(globals.possible_destination))
                    globals.goal = goal
                    relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
                    state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1])
    q_table = globals.q_table
    if state not in q_table or random.uniform(0, 1) < 0.1:
        action = random.randint(0, 5)
    else:
        action = np.argmax(q_table[state])
    globals.prev_taxi_pos = taxi_pos
    globals.prev_action = action
    return action
    # You can submit this random agent to evaluate the performance of a purely random strategy.


# def get_action(obs):
    
#     # TODO: Train your own agent
#     # HINT: If you're using a Q-table, consider designing a custom key based on `obs` to store useful information.
#     # NOTE: Keep in mind that your Q-table may not cover all possible states in the testing environment.
#     #       To prevent crashes, implement a fallback strategy for missing keys. 
#     #       Otherwise, even if your agent performs well in training, it may fail during testing.

#     taxi_row, taxi_col, R_x, R_y, G_x, G_y, Y_x, Y_y, B_x, B_y, obstacle_north, obstacle_south, obstacle_east, obstacle_west, passenger_look, destination_look = obs
#     if globals.goal is None:
#         station = [(R_x, R_y), (G_x, G_y), (Y_x, Y_y), (B_x, B_y)]
#         goal = find_nearest_station((taxi_row, taxi_col), station)
#         globals.goal = goal
#         globals.possible_passenger = set(station)
#         globals.possible_destination = set(station)
#         globals.has_passenger = False
#         taxi_pos = (taxi_row, taxi_col)
#         relative_goal_pos = (goal[0] - taxi_pos[0], goal[1] - taxi_pos[1])
#         state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)
#     else:
#         taxi_row, taxi_col, _,_,_,_,_,_,_,_,obstacle_north, obstacle_south, obstacle_east, obstacle_west, passenger_look, destination_look = obs

#         taxi_pos = (taxi_row, taxi_col)
#         prev_taxi_pos = globals.prev_taxi_pos

#         adjacent = set([(taxi_row + 1, taxi_col), (taxi_row - 1, taxi_col), (taxi_row, taxi_col + 1), (taxi_row, taxi_col - 1), (taxi_row, taxi_col)])

#         if passenger_look:
#             globals.possible_passenger.intersection_update(adjacent)
#         else:
#             globals.possible_passenger.difference_update(adjacent)

#         if destination_look:
#             globals.possible_destination.intersection_update(adjacent)
#         else:
#             globals.possible_destination.difference_update(adjacent)

#         if globals.has_passenger == False:
#             if len(globals.possible_passenger) == 1:
#                 if prev_taxi_pos in globals.possible_passenger and globals.prev_action == 4:
#                     globals.has_passenger = True
#                     globals.possible_passenger = set()
#                     goal = list(globals.possible_destination)[0]
#                     globals.goal = goal
#                     relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
#                     state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)
#                 else:
#                     goal = list(globals.possible_passenger)[0]
#                     globals.goal = goal
#                     relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
#                     state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)
#             else:
#                 if globals.goal in globals.possible_passenger:
#                     goal = globals.goal
#                     relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
#                     state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)
#                 else:
#                     goal = find_nearest_station(taxi_pos, list(globals.possible_passenger))
#                     globals.goal = goal
#                     relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
#                     state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)

#         else: # has_passenger == True
#             if globals.prev_action == 5:
#                 globals.has_passenger = False
#                 globals.possible_passenger = {taxi_pos}
#                 goal = taxi_pos
#                 globals.goal = goal
#                 relative_goal_pos = (0, 0)
#                 state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)
#             else:
#                 if globals.goal in globals.possible_destination:
#                     goal = globals.goal
#                     relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
#                     state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)
#                 else:
#                     goal = find_nearest_station(taxi_pos, list(globals.possible_destination))
#                     globals.goal = goal
#                     relative_goal_pos = (goal[0] - taxi_row, goal[1] - taxi_col)
#                     state = ( obstacle_south, obstacle_north, obstacle_east, obstacle_west, relative_goal_pos[0], relative_goal_pos[1], globals.has_passenger)

    
    # print(f"Goal Pos: {goal}, Possible Passenger: {globals.possible_passenger}, Possible Destination: {globals.possible_destination}, Has Passenger: {globals.has_passenger}")