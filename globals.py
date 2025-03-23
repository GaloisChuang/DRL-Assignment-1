import pickle

goal = None
possible_passenger = set()
possible_destination = set()
has_passenger = False
prev_taxi_pos = None
prev_action = None
fuel = 5000

with open('q_table.pkl', 'rb') as f:
    q_table = pickle.load(f)