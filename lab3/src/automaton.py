def build_simple_automaton(L):
    transitions = {0: {s: 1 for s in L}}
    return transitions
