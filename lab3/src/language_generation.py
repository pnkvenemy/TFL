import itertools
import re

def generate_language(Φ, length):
    return set(''.join(p) for p in itertools.product(Φ, repeat=length))

def expand_alphabet(Φ, Σ, C, P):
    
    for new_symbol in Σ - Φ: 
        new_Φ = Φ | {new_symbol}
        P_new_Φ = generate_language(new_Φ, 2)
        S_new_Φ = generate_language(new_Φ, 2)
        if not is_regular(P_new_Φ, C, P) or not is_regular(S_new_Φ, C, P):
            return Φ 
        Φ = new_Φ
    return Φ

def generate_regex(L):
    return '|'.join(map(re.escape, L))

def build_simple_automaton(L):
    transitions = {0: {s: 1 for s in L}}
    return transitions

def is_regular(L, C, P):
    
    regex = generate_regex(L)
    automaton = build_simple_automaton(L)

    for s in L:
        if not re.fullmatch(regex, s):
            return False

    repeated_substrings = set()
    for s in L:
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                substring = s[i:j]
                if s.count(substring) > 1:
                    repeated_substrings.add(substring)

    states = set()
    for word in L:
        for state in automaton.keys():
            if all(char in automaton[state] for char in word):
                states.add(state)

    return len(repeated_substrings) <= C * P and len(states) <= C * P
