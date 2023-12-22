import itertools
import re

def find_pumping(L):
    pumpings = set()
    for s in L:
        matches = re.finditer(r'(.)\1*', s)
        for match in matches:
            u, v = s[:match.start()], s[match.start():match.end()]
            if u and v: 
                pumpings.add((u, v))
    return pumpings

def check_combined_pumping(L, pumpings_P, pumpings_S, P_prime):
    max_iterations = 3 

    for k1, k2 in itertools.product(range(1, max_iterations + 1), repeat=2):
        for (u_P, v_P), (u_S, v_S) in itertools.product(pumpings_P, pumpings_S):
            for i in range(1, k1 + 1):
                for j in range(1, k2 + 1):
                    potential_word = u_P + (v_P * i) + u_S + (v_S * j)
                    if potential_word in L:
                        return True
    return False
