
#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi

class DFA:
    def __init__(self):
        self.states = []
        self.alphabets = []
        self.start_state = ""
        self.accept_states = []
        self.transitions = {}