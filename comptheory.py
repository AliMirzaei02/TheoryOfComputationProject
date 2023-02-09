import networkx as netx
from collections import defaultdict, deque

class auto:
    class DFA():
        def __init__(self, states:set, alphabet:set, initial:str, transition:dict, Accept:set):
            self.states = states
            self.alphabet =alphabet
            self.initial = initial
            self.transition = transition
            self.Accept = Accept
            print('constructed a new DFA.')
        
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
            for start_state, transition in self.transition.items()
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
            
        def maxstringlength(self):
            if self.NullCheck(): return 0
            if not self.FiniteCheck(): return "the language is not finite."
            else:
                graph=netx.DiGraph([(start_state, end_state)
                for start_state, transition in self.transitions.items()
                for end_state in transition.values()])
                states=netx.descendants(graph, self.initial)
                Reachable2Accept=self.Accept.union(*(netx.ancestors(graph,state)for state in self.Accept))
                commonstates=states.intersection(Reachable2Accept)
                sub=graph.subgraph(commonstates)
                return netx.dag_longest_path_length(sub) 
            
        def minstringlength(self):
            queue = deque()
            distances = defaultdict(lambda: None)
            distances[self.initial] = 0
            queue.append(self.initial)
            while queue:
                state = queue.popleft()
                
                if state in self.Accept:
                    return distances[state]
                for next_state in self.transition[state].values():
                    if distances[next_state] is None:
                        distances[next_state] = distances[state] + 1
                        queue.append(next_state)
            return 0
        
        def Complement(self):
            NewAccept=set()
            for state in self.states:
                if state not in self.Accept: NewAccept.add(state)
            NewDFA=auto.DFA(self.states,self.alphabet,self.initial,self.transition, NewAccept)
            return NewDFA
        
        def NewDFA(dfa1,dfa2):
            if dfa1.alphabet != dfa2.alphabet: raise Exception('input symbols do not match!')
            newstates={}
            for state1 in dfa1:
                for state2 in dfa2:
                    newstates.add(state1+state2)
            newinitial=dfa1.initial+dfa2.initial
            usefulstates={newinitial}
            visited=[newinitial]
            while len(visited)>0:
                state=visited.pop(0)
                
        
        def Union(self,other)->self:
            