#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi
import networkx as nx
from collections import defaultdict, deque

class DFA:
    def __init__(self, states=set(), alphabets=set(), initial_state=str(), accept_states=set(), transitions=dict()):
        self.states = states
        self.alphabets = alphabets
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.transitions = transitions
    
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
            
    def isInfinite(self):
        if self.isNull(): return False
        graph = nx.DiGraph([(start_state, end_state)
        for start_state, transition in self.transitions.items()
        for end_state in transition.values()])
        states = nx.descendants(graph, self.initial_state)
        Reachable2Accept = self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
        commonstates = states.intersection(Reachable2Accept)
        sub = graph.subgraph(commonstates)
            
        try:
            longest=nx.dag_longest_path_length(sub)
            return False
        except:
            return True 
        
        
    def maxstringlength(self):
        if self.isNull(): return 0
        elif self.isInfinite(): return "The language is infinite."
        else:
            graph=nx.DiGraph([(start_state, end_state)
            for start_state, transition in self.transitions.items()
            for end_state in transition.values()])
            states=nx.descendants(graph, self.initial_state)
            Reachable2Accept=self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
            commonstates=states.intersection(Reachable2Accept)
            sub=graph.subgraph(commonstates)
            return nx.dag_longest_path_length(sub) + 1
            
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
                
        
    def Union(self,other):
        pass
        
    def Difference(self,other):
        pass
        
    def Intersection(self,other):
        pass



#   A DFA that accept strings '*aa'
dfa1 = DFA()

dfa1.add_state('0')
dfa1.add_state('1')
dfa1.add_state('2')

dfa1.add_alphabet('a')
dfa1.add_alphabet('b')

dfa1.add_initial_state('0')

dfa1.add_accept_state('2')

dfa1.add_transition('0', 'a', '1')
dfa1.add_transition('0', 'b', '0')
dfa1.add_transition('1', 'a', '2')
dfa1.add_transition('1', 'b', '0')
dfa1.add_transition('2', 'a', '2')
dfa1.add_transition('2', 'b', '0')

dfa1.printDFA()

print(dfa1.isAccept('aaaabaa'))

print(dfa1.isNull())

print(dfa1.isInfinite())

print(dfa1.maxstringlength())

print(dfa1.minstringlength())



#   A DFA that accept strings 'b*'
dfa2 = DFA({'0', '1', '2'}               #states
            , {'a','b'}                  #alphabet
            , '0'                        #initial state
            , {'1'}                      #accept_states
            ,{'0': {'a': '2', 'b': '1'}  #transitions
            , '1': {'a': '1', 'b': '1'}  #transitions
            , '2': {'a': '2', 'b': '2'}})#transitions

dfa2.printDFA()

print(dfa2.isAccept('bbaba'))

print(dfa2.isNull())

print(dfa2.isInfinite())

print(dfa2.maxstringlength())

print(dfa2.minstringlength())