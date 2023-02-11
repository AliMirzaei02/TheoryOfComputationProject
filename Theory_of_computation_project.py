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

        self.Union = self.__Union
        self.Difference = self.__Difference
        self.Intersection = self.__Intersection
        self.isSubset = self.__isSubset
        self.isDisjoint = self.__isDisjoint


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


    def toGraph(self):
        return nx.DiGraph([(start_state, dest_state) for start_state, transition in self.transitions.items() for dest_state in transition.values()])


    def reachableStates(self):
        visited = set(self.initial_state)
        states = deque([self.initial_state])
        while states:
            state = states.popleft()
            for next_state in self.transitions[state].values():
                if next_state not in visited:
                    visited.add(next_state)
                    states.append(next_state)
        return visited


    def printDFA(self):
        print("states are:        ", self.states)
        print("alphabets are:     ", self.alphabets)
        print("initial_state is:  ", self.initial_state)
        print("accept_states are: ", self.accept_states)
        print("transitions are:   ", self.transitions, "\n")


    def isAccept(self, test_string:str):
            state = self.initial_state
            for symbol in test_string:
                state = self.transitions[state][symbol]
            if state in self.accept_states: return True
            else: return False


    def isNull(self):
        for reachable in self.reachableStates():
            #print(reachable)
            if reachable in self.accept_states:
                return False
        return True


    def isInfinite(self):
        if self.isNull(): return False
        graph = self.toGraph()
        states = nx.descendants(graph, self.initial_state)
        Reachable2Accept = self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
        commonstates = states.intersection(Reachable2Accept)
        sub = graph.subgraph(commonstates)
        try:
            longest = nx.dag_longest_path_length(sub)
            return False
        except:
            return True 


    def acceptStringLength(self):
        if not(self.isInfinite() or self.isNull()):
            max_string_length = self.maxstringlength()
            if max_string_length:
                min_string_length = self.minstringlength()
                dfa_graph = self.toGraph()
                count = 0
                for word_length in range(min_string_length, max_string_length + 1):
                    for accept_state in self.accept_states:
                        paths = nx.all_simple_paths(dfa_graph, self.initial_state, accept_state)
                        for path in paths:
                            if len(path) == word_length:
                                count += 1
                return count
        elif self.isNull(): return None
        else: return "Infinite!"


    def maxstringlength(self):
        if self.isNull(): return 0
        elif self.isInfinite(): return "Infinite!"
        else:
            graph = self.toGraph()
            states=nx.descendants(graph, self.initial_state)
            Reachable2Accept=self.accept_states.union(*(nx.ancestors(graph,state)for state in self.accept_states))
            commonstates=states.intersection(Reachable2Accept)
            sub=graph.subgraph(commonstates)
            return nx.dag_longest_path_length(sub) + 1


    def minstringlength(self):
        queue = deque([self.initial_state])
        distances = defaultdict(lambda: None)
        distances[self.initial_state] = 0
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
        newDFA = DFA(self.states, self.alphabets, self.initial_state, NewAccept, self.transitions)
        return newDFA


    def NewDFA(self,dfa2):
            seen=[]
            if self.alphabets != dfa2.alphabets: raise Exception('input symbols do not match!')
            newinitial=self.initial_state+'_'+dfa2.initial_state
            usefulstates={newinitial}
            visited=[newinitial]
            newtransitions={}
            while len(visited)>0:
                state=visited.pop(0)
                for symbol in self.alphabets:
                    nextdfastate=self.transitions[state.split('_')[0]][symbol]+'_'+dfa2.transitions[state.split('_')[1]][symbol]
                    newtransitions[state]=newtransitions.get(state,{})
                    newtransitions[state][symbol]=nextdfastate
                    if nextdfastate not in seen:
                        visited.append(nextdfastate)
                    usefulstates.add(nextdfastate)
                seen.append(state)
            return usefulstates,newinitial,newtransitions


    def __Union(self,other):
        newstates, newinitial, newtransitions = self.NewDFA(other)
        newaccepts = set()
        newDFA = DFA(newstates, self.alphabets, newinitial, newaccepts, newtransitions)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in self.accept_states or state2 in other.accept_states:
                if state in newDFA.reachableStates():
                    newDFA.add_accept_state(state1+'_'+state2)
        return newDFA

    @classmethod
    def Union(cls,dfa1,dfa2):
        newstates, newinitial, newtransitions = dfa1.NewDFA(dfa2)
        newaccepts = set()
        newDFA = DFA(newstates, dfa1.alphabets, newinitial, newaccepts, newtransitions)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in dfa1.accept_states or state2 in dfa2.accept_states:
                if state in newDFA.reachableStates():
                    newDFA.add_accept_state(state1+'_'+state2)
        return newDFA


    def __Difference(self,other):
        newstates, newinitial, newtransitions = self.NewDFA(other)
        newaccepts = set()
        newDFA = DFA(newstates, self.alphabets, newinitial, newaccepts, newtransitions)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in self.accept_states and state2 not in other.accept_states:
                if state in newDFA.reachableStates():
                    newDFA.add_accept_state(state1+'_'+state2)
        return newDFA

    @classmethod
    def Difference(cls,dfa1,dfa2):
        newstates, newinitial, newtransitions = dfa1.NewDFA(dfa2)
        newaccepts = set()
        newDFA = DFA(newstates, dfa1.alphabets, newinitial, newaccepts, newtransitions)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in dfa1.accept_states and state2 not in dfa2.accept_states:
                if state in newDFA.reachableStates():
                    newDFA.add_accept_state(state1+'_'+state2)
        return newDFA


    def __Intersection(self,other):
        newstates, newinitial, newtransitions = self.NewDFA(other)
        newaccepts = set()
        newDFA = DFA(newstates, self.alphabets, newinitial, newaccepts, newtransitions)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in self.accept_states and state2 in other.accept_states:
                if state in newDFA.reachableStates():
                    newDFA.add_accept_state(state1+'_'+state2)
        return newDFA

    @classmethod
    def Intersection(cls,dfa1,dfa2):
        newstates, newinitial, newtransitions = dfa1.NewDFA(dfa2)
        newaccepts = set()
        newDFA = DFA(newstates, dfa1.alphabets, newinitial, newaccepts, newtransitions)
        for state in newstates:
            state1, state2 = state.split('_')
            #print(state1)
            #print(state2)
            if state1 in dfa1.accept_states and state2 in dfa2.accept_states:
                if state in newDFA.reachableStates():
                    newDFA.add_accept_state(state1+'_'+state2)
        return newDFA


    def __isSubset(self, other):
        #self.Difference(other).printDFA()
        return not len(self.Difference(other).accept_states)

    @classmethod
    def isSubset(cls,dfa1,dfa2):
        #self.Difference(other).printDFA()
        return not len(DFA.Difference(dfa1, dfa2).accept_states)


    def __isDisjoint(self, other):
        #self.Intersection(other).printDFA()
        return not len(self.Intersection(other).accept_states)

    @classmethod
    def isDisjoint(cls,dfa1,dfa2):
        #self.Intersection(other).printDFA()
        return not len(DFA.Intersection(dfa1, dfa2).accept_states)


    def deltastar(self,state,string2check):
        for symbol in string2check:
            state= self.transitions[state][symbol]
        return state

    def minimize(self):
        flag=False
        DFAacceptstates=list(self.accept_states)
        DFAnonacceptstates=list(self.states - self.accept_states)
        nthEquivalence=[[DFAnonacceptstates,DFAacceptstates]]
        n=0
        eq=False
        while True:
            eqclass=[]
            l=[]
            for i in nthEquivalence[n]:
                l.append(i[0])
            eqclass.append([l])    
            for i in range(len(nthEquivalence[n])):
                for state in nthEquivalence[n][i][1:] :
                    eq=True
                    for sym in self.alphabets:
                        stateofeqclass=self.deltastar(eqclass[i],sym)
                        stateofstate=self.deltastar(state,sym)
                        for lists in nthEquivalence[n]:
                            if stateofeqclass in lists:
                                if stateofstate in lists:
                                    eq=True
                                else:
                                    eq=False
                                    break
                        if not eq:
                            if len(nthEquivalence)==n+1: 
                                nthEquivalence.append([[x for x in eqclass[i]],[state]])
                                break
                            flag1=bool
                            for checkstate in nthEquivalence[n+1]:
                                for symbol in self.alphabets:
                                    stateofstate=self.deltastar(state,symbol)
                                    stateofcheckstate=self.deltastar(checkstate[0],symbol)
                                    for checklists in nthEquivalence[n]:
                                        if stateofstate in checklists:
                                            if stateofcheckstate in checklists:
                                                flag1=True
                                            else:
                                                flag1=False
                                                break
                                    if not flag1:break    
                                if flag1: 
                                    checkstate.append(state)
                                    break
                            else: nthEquivalence[n+1].append(state)
                    if eq:
                        if len(nthEquivalence)==n+1: 
                            nthEquivalence.append([[x for x in eqclass[i]]])
                        for nextlists in nthEquivalence[n+1]:
                            if eqclass[i] in nextlists:nextlists.append(state)
                                                 
            if nthEquivalence[n] == nthEquivalence[n+1]:break
            n+=1  
        newstates=nthEquivalence[n]
        neweq=[]
        for lists in newstates:
            neweq.append(lists[0])
        for states in newstates:
            if self.initial_state in states:newinitial= states
        newaccept=[]
        for accept in self.accept_states:
            for states in newstates:
                if accept in states: newaccept.append(states)
        newtransition={}
        for state in neweq:
            for sym in self.alphabets:
                goesto=self.deltastar(state,sym)
                for lists in newstates:
                    if state in lists:
                        for lists2 in newstates:
                            if goesto in lists2:
                                newtransition['_'.join(lists)]=newtransition.get('_'.join(lists),{})
                                newtransition['_'.join(lists)][sym]='_'.join(lists2)
        newstates=['_'.join(x) for x in newstates]
        newaccept=['_'.join(x) for x in newaccept]
        newinitial='_'.join(newinitial)
        newDFA=DFA(newstates,self.alphabets,newinitial,newaccept,newtransition)                     
        return     newDFA


####################################################
###                 DFA Objects                  ###
##                                                ##
#                                                  #

#   A DFA that accepts strings that end with aa
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


#   A DFA that accepts strings that do not contain b
dfa2 = DFA({'0', '1', '2'},            #states
           {'a','b'},                  #alphabet
            '0',                       #initial state
           {'1'},                      #accept_states
           {'0': {'a': '1', 'b': '2'}, #transitions
            '1': {'a': '1', 'b': '2'}, #transitions
            '2': {'a': '2', 'b': '2'}})#transitions


#   A DFA that accepts strings that do not contain a
dfa3 = DFA({'0', '1', '2'},            #states
           {'a','b'},                  #alphabet
            '0',                       #initial state
           {'1'},                      #accept_states
           {'0': {'a': '2', 'b': '1'}, #transitions
            '1': {'a': '2', 'b': '1'}, #transitions
            '2': {'a': '2', 'b': '2'}})#transitions


#   A DFA that accepts strings that contain ba    ?
dfa4 = DFA({'0', '1', '2', '3'},       #states
           {'a', 'b'},                 #alphabet
            '0',                       #initial state
           {'3'},                      #Accept state
           {'0': {'a': '1', 'b': '2'}, #transitions
            '1': {'a': '1', 'b': '0'}, #transitions
            '2': {'a': '3', 'b': '0'}, #transitions
            '3': {'a': '3', 'b': '3'}})#transitions


#   A DFA that accepts strings that end with a
dfa5 = DFA({'0','1'},              #states
           {'a','b'},              #alphabet
            '0',                   #initial state
           {'1'},                  #Accept state
           {'0':{'a':'1','b':'0'}, #transitions
            '1':{'a':'1','b':'0'}})#transitions


#   A DFA that accepts strings that start with b
dfa6 = DFA({'0','1','2'},          #states
           {'a','b'},              #alphabet
            '0',                   #initial state
           {'1'},                  #Accept state
           {'0':{'a':'2','b':'1'}, #transitions
            '1':{'a':'1','b':'1'}, #transitions
            '2':{'a':'2','b':'2'}})#transitions

print("DFA1 is:")
dfa1.printDFA()
print("DFA2 is:")
dfa2.printDFA()
print("DFA3 is:")
dfa3.printDFA()
print("DFA4 is:")
dfa4.printDFA()
print("DFA5 is:")
dfa5.printDFA()
print("DFA6 is:")
dfa6.printDFA()

print()

print("DFA1 isAccept abababaa? ", dfa1.isAccept("abababaa"))
print("DFA2 isAccept aaabaaaaa? ", dfa2.isAccept("aaabaaaaa"))
print("DFA3 isAccept bbb? ", dfa3.isAccept("bbb"))
print("DFA4 isAccept abababbaabaabb? ", dfa4.isAccept("abababbaabaabb"))
print("DFA5 isAccept babababa? ", dfa5.isAccept("babababa"))
print("DFA6 isAccept abaabbaa? ", dfa6.isAccept("abaabbaa"))

print()

print("DFA1 isNull? ", dfa1.isNull())
print("DFA2 isNull? ", dfa2.isNull())
print("DFA3 isNull? ", dfa3.isNull())
print("DFA4 isNull? ", dfa4.isNull())
print("DFA5 isNull? ", dfa5.isNull())
print("DFA6 isNull? ", dfa6.isNull())

print()

print("DFA1 isInfinite? ", dfa1.isInfinite())
print("DFA2 isInfinite? ", dfa2.isInfinite())
print("DFA3 isInfinite? ", dfa3.isInfinite())
print("DFA4 isInfinite? ", dfa4.isInfinite())
print("DFA5 isInfinite? ", dfa5.isInfinite())
print("DFA6 isInfinite? ", dfa6.isInfinite())

print()

print("What's acceptStringLength for DFA1? ", dfa1.acceptStringLength())
print("What's acceptStringLength for DFA2? ", dfa2.acceptStringLength())
print("What's acceptStringLength for DFA3? ", dfa3.acceptStringLength())
print("What's acceptStringLength for DFA4? ", dfa4.acceptStringLength())
print("What's acceptStringLength for DFA5? ", dfa5.acceptStringLength())
print("What's acceptStringLength for DFA6? ", dfa6.acceptStringLength())

print()

print("What's maxstringlength for DFA1? ", dfa1.maxstringlength())
print("What's maxstringlength for DFA2? ", dfa2.maxstringlength())
print("What's maxstringlength for DFA3? ", dfa3.maxstringlength())
print("What's maxstringlength for DFA4? ", dfa4.maxstringlength())
print("What's maxstringlength for DFA5? ", dfa5.maxstringlength())
print("What's maxstringlength for DFA6? ", dfa6.maxstringlength())

print()

print("What's minstringlength for DFA1? ", dfa1.minstringlength())
print("What's minstringlength for DFA2? ", dfa2.minstringlength())
print("What's minstringlength for DFA3? ", dfa3.minstringlength())
print("What's minstringlength for DFA4? ", dfa4.minstringlength())
print("What's minstringlength for DFA5? ", dfa5.minstringlength())
print("What's minstringlength for DFA6? ", dfa6.minstringlength())

print()

print("DFA1 Complement is:")
dfa1.Complement().printDFA()
print("DFA2 Complement is:")
dfa2.Complement().printDFA()
print("DFA3 Complement is:")
dfa3.Complement().printDFA()
print("DFA4 Complement is:")
dfa4.Complement().printDFA()
print("DFA5 Complement is:")
dfa5.Complement().printDFA()
print("DFA6 Complement is:")
dfa6.Complement().printDFA()


print("Union of dfa5 and dfa6 is:")
dfa5.Union(dfa6).printDFA()
print("Union of dfa5 and dfa6 isAccept ababa? ", DFA.Union(dfa5, dfa6).isAccept('ababa'), "\n\n")

print("Difference of dfa4 and dfa3 is:")
dfa4.Difference(dfa3).printDFA()
print("Difference of dfa4 and dfa3 isAccept bb? ", DFA.Difference(dfa4, dfa3).isAccept('bb'), "\n\n")

print("Intersection of dfa1 and dfa2 is:")
dfa1.Intersection(dfa2).printDFA()
print("Intersection of dfa1 and dfa2 isAccept a? ", DFA.Intersection(dfa1, dfa2).isAccept('a'), "\n\n")


print("DFA1 isSubset of DFA5? ", dfa1.isSubset(dfa5))

print()

print("DFA3 and DFA2 are isSubset? ", DFA.isDisjoint(dfa3, dfa2))

dfa2=dfa2.minimize()
dfa2.printDFA()