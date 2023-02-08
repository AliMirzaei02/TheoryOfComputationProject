from comptheory import auto

dfa=auto.DFA({'q0','q1','q2','q3'}#states
            ,{'a','b'}#alphabet
            ,'q0'#initial state
            ,{'q0':{'a':'q1','b':'q2'}#transitions
            ,'q1':{'a':'q1','b':'q0'}#transitions
            ,'q2':{'a':'q3','b':'q0'}#transitions
            ,'q3':{'a':'q3','b':'q3'}}#transitions
            ,{'q3'})#Accept state
if dfa.checkstring('b'):
    print('Accepted')
else: print('Rejected')
