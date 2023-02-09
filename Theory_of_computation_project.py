#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi
import networkx as nx
from collections import defaultdict, deque

class DFA:
    def __init__(self):
        self.states = set()
        self.alphabets = set()
        self.initial_state = str()
        self.accept_states = set()
        self.transitions = dict()
    
    def add_state(self, state):
        self.states.add(state)

    def add_alphabet(self, alpha):
        self.alphabets.add(alpha)

    def add_initial_state(self, initial_state):
        self.initial_state = initial_state

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
        print("initial_state is:  ", self.initial_state)
        print("accept_states are: ", self.accept_states)
        print("transitions are:   ", self.transitions)

    def isAccept(self, test_string:str):
            state = self.initial_state
            for symbol in test_string:
                state = self.transitions[state][symbol]
            if state in self.accept_states: return True
            else: return False
        
    def isNull(self):
        visited = [self.initial_state]
        states = [self.initial_state]
        while len(states)>0:
            state = states[0]
            del states[0]
            for next_state in self.transitions[state].values():
                if next_state not in visited: 
                    if next_state in self.accept_states: return False
                    visited.append(next_state)
                    states.append(next_state)
        return True
            
    def isFinite(self):
        if self.isNull(): return True
        graph = nx.DiGraph([(start_state, end_state)
        for start_state, transition in self.transitions.items()
        for end_state in transition.values()])
        states = nx.descendants(graph, self.initial_state)
        Reachable2Accept = self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
        commonstates = states.intersection(Reachable2Accept)
        sub = graph.subgraph(commonstates)
            
        try:
            longest=nx.dag_longest_path_length(sub)
            return True
        except:
            return False 
        
        
    def maxstringlength(self):
        if self.isNull(): return 0
        if not self.isFinite(): return "the language is not finite."
        else:
            graph=nx.DiGraph([(start_state, end_state)
            for start_state, transition in self.transitions.items()
            for end_state in transition.values()])
            states=nx.descendants(graph, self.initial_state)
            Reachable2Accept=self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
            commonstates=states.intersection(Reachable2Accept)
            sub=graph.subgraph(commonstates)
            return nx.dag_longest_path_length(sub) 
            
    def minstringlength(self):
        queue = deque()
        distances = defaultdict(lambda: None)
        distances[self.initial_state] = 0
        queue.append(self.initial_state)
        while queue:
            state = queue.popleft()            
            if state in self.accept_states:
                return distances[state]
            for next_state in self.transitions[state].values():
                if distances[next_state] is None:
                    distances[next_state] = distances[state] + 1
                    queue.append(next_state)
        return 0
        
    def Complement(self):
        NewAccept=set()
        for state in self.states:
            if state not in self.accept_states: NewAccept.add(state)
        NewDFA=DFA(self.states,self.alphabets,self.initial_state,self.transitions, NewAccept)
        return NewDFA
        
    def NewDFA(dfa1,dfa2):
        if dfa1.alphabets != dfa2.alphabets: raise Exception('input symbols do not match!')
        newinitial=dfa1.initial_state+'_'+dfa2.initial_state
        usefulstates={newinitial}
        visited=[newinitial]
        while len(visited)>0:
            state=visited.pop(0)
            for symbol in dfa1.alphabets:
                nextdfastate=dfa1.transitions[state.split('_')[0]][symbol]+'_'+dfa2.transitions[state.split('_')[1]][symbol]
                usefulstates.add(nextdfastate)
                visited.append(nextdfastate)
                    
        return usefulstates,newinitial
                
        
    def Union(self,other)->self:
        pass
        
    def Difference(self,other)->self:
        pass
        
    def Intersection(self,other)->self:
        pass



#   A DFA that accept strings '*aa'
dfa = DFA()

dfa.add_state('0')
dfa.add_state('1')
dfa.add_state('2')

dfa.add_alphabet('a')
dfa.add_alphabet('b')

dfa.add_initial_state('0')

dfa.add_accept_state('2')

dfa.add_transition('0', 'a', '1')
dfa.add_transition('0', 'b', '0')
dfa.add_transition('1', 'a', '2')
dfa.add_transition('1', 'b', '0')
dfa.add_transition('2', 'a', '2')
dfa.add_transition('2', 'b', '0')

dfa.printDFA()

print(dfa.isAccept('aaaabaa'))

print(dfa.isNull())

print(dfa.isFinite())