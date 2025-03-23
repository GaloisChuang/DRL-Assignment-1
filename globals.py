import pickle

goal = None
possible_passenger = set()
possible_destination = set()
has_passenger = False
prev_taxi_pos = None
with open('q_table.pkl', 'rb') as f:
    q_table = pickle.load(f)
prev_action = None