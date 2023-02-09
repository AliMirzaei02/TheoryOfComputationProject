
#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi

class DFA:
    def __init__(self):
        self.states = set()
        self.alphabets = set()
        self.start_state = str()
        self.accept_states = set()
        self.transitions = dict()
    
    def add_state(self, state):
        self.states.add(state)

    def add_alphabet(self, alpha):
        self.alphabets.add(alpha)

    def add_start_state(self, start_state):
        self.start_state = start_state

    def add_accept_state(self, accept_state):
        self.accept_states.add(accept_state)

    def add_transition(self, state, alpha, dest):
        if state in self.transitions:
            self.transitions[state][alpha] = dest
        else:
            self.destination = {}
            self.destination[alpha] = dest
            self.transitions[state] = self.destination

    def printDFA(self):
        print("states are:        ", self.states)
        print("alphabets are:     ", self.alphabets)
        print("start_state is:    ", self.start_state)
        print("accept_states are: ", self.accept_states)
        print("transitions are:   ", self.transitions)

    def checkstring(self, string2check:str):
            state=self.initial
            for symbol in string2check:
                state=self.transition[state][symbol]
                print(state)
            if state in self.Accept: return True
            return False
        
    def NullCheck(self):
        visited=[self.initial]
        states=[self.initial]
        while len(states)>0:
            state=states[0]
            del states[0]
            for next_state in self.transition[state].values():
                if next_state not in visited: 
                    if next_state in self.Accept: return False
                    visited.append(next_state)
                    states.append(next_state)
        return True
            
    def FiniteCheck(self):
        if self.NullCheck(): return True
        graph=netx.DiGraph([(start_state, end_state)
        for start_state, transition in self.transitions.items()
        for end_state in transition.values()])
        states=netx.descendants(graph, self.initial)
        Reachable2Accept=self.Accept.union(*(netx.ancestors(graph,state)for state in self.Accept))
        commonstates=states.intersection(Reachable2Accept)
        sub=graph.subgraph(commonstates)
            
        try:
            longest=netx.dag_longest_path_length(sub)
            return True
        except:
            return False 




#   A DFA that accept strings '*aa'
dfa = DFA()

dfa.add_state('0')
dfa.add_state('1')
dfa.add_state('2')

dfa.add_alphabet('a')
dfa.add_alphabet('b')

dfa.add_start_state('0')

dfa.add_accept_state('2')

dfa.add_transition('0', 'a', '1')
dfa.add_transition('0', 'b', '0')
dfa.add_transition('1', 'a', '2')
dfa.add_transition('1', 'b', '0')
dfa.add_transition('2', 'a', '2')
dfa.add_transition('2', 'b', '0')

dfa.printDFA()

dfa.isAccept('aaaabaa')

dfa.isEmpty()