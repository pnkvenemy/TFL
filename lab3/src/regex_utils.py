import re

def generate_regex(L):
    return '|'.join(map(re.escape, L))
