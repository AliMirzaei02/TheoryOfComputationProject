
#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi

class DFA:
    def __init__(self):
        self.states = []
        self.alphabets = []
        self.start_state = ""
        self.accept_states = []
        self.transitions = {}
    
    def add_state(self, state):
        self.states.append(state)

    def add_alphabet(self, alpha):
        self.alphabets.append(alpha)

    def add_start_state(self, start_state):
        self.start_state = start_state

    def add_accept_state(self, accept_state):
        self.accept_states.append(accept_state)

    def add_transition(self, state, alpha, dest):
        self.transitions[(state, alpha)] = dest
