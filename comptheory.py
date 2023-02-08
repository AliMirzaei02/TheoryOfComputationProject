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
            
            
        