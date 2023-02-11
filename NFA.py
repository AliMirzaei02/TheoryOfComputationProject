#   TheoryOfComputationProject by Ali mirzaei and Bardia Vahedi
from collections import deque
from DFA import DFA

class NFA:
    def __init__(self, states=set(), alphabets=set(), initial_state=str(), accept_states=set(), transitions=dict()):
        self.states = states
        self.alphabets = alphabets.add("λ")
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.transitions = transitions


    def getLambdaClosure(self, state):
        visited = set(state)
        states = deque([state])
        while states:
            cur_state = states.popleft()
            for next_state in self.transitions[cur_state]["λ"]:
                if next_state not in visited:
                    visited.add(next_state)
                    states.append(next_state)
        return visited


    def getNewState(self, state_list):
        new_state = str()
        for single_state in state_list:
            new_state += single_state
        return new_state


    def isAcceptState(self, state_list):
        for single_state in state_list:
            for accept_state in self.accept_states:
                if single_state == accept_state:
                    return True
        return False


    def nfaToDfa(self):
        dfa = DFA(alphabets=self.alphabets)
        lambda_closure = dict()
        for single_state in self.states:
            lambda_closure[single_state] = self.getLambdaClosure(single_state)
        dfa.add_initial_state(self.getNewState(lambda_closure[self.initial_state]))
        if self.isAcceptState(lambda_closure[self.initial_state]):
            dfa.add_accept_state(self.getNewState(lambda_closure[self.initial_state]))
        dfa_deque = deque(lambda_closure[self.initial_state])

        while dfa_deque:
            cur_state = dfa_deque.popleft()
            for alpha in self.alphabets:
                from_closure = set()
                for next_state in cur_state:
                    from_closure.update(set(self.transitions[next_state][alpha]))
                if from_closure:
                    to_state = set()
                    for state in from_closure:
                        to_state.update(set(lambda_closure[self.states[state]]))
                    if to_state not in dfa.states:
                        dfa_deque.append(to_state)
                        dfa.add_state(self.getNewState(to_state))
                        if self.isAcceptState(to_state):
                            dfa.add_accept_state(self.getNewState(to_state))
                    dfa.add_transition(self.getNewState(cur_state), alpha, self.getNewState(to_state))
                else:
                    if "ϕ" not in dfa.states:
                        dfa.add_state("ϕ")
                        for alpha in self.alphabets:
                            dfa.add_transition("ϕ", alpha, "ϕ")
                    dfa.add_transition(self.getNewState(cur_state), alpha, self.getNewState(to_state))


