import networkx as netx

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
            for start_state, transition in self.transitions.items()
            for end_state in transition.values()])
            states=netx.descendants(graph, self.initial)
            Reachable2Accept=self.Accept.union(*(netx.ancestors(graph,state)for state in self.Accept))
            commonstates=states.intersection(Reachable2Accept)
            sub=graph.subgraph(commonstates)
            # from here
            try:
                longest=netx.dag_longest_path_length(sub)
                return True
            except:
                return False 
            
        