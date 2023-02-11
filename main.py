from DFA import DFA
from NFA import NFA

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

