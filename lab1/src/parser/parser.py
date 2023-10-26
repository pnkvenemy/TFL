import re

from models.linear import LinFunc


def parse(file):
    string_pairs = parse_raw(file)
    func_pairs, names_set = translate(string_pairs)
    return func_pairs, names_set

def parse_raw(file):
    with open(file) as f:
        srs_string = f.read()

    regex = r'^\s*[a-z]+\s*->\s*[a-z]+\s*'
    elems = []
    while srs_string:
        m = re.findall(regex, srs_string)
        if not m:
            raise RuntimeError('данные не соответствуют синтаксису')
        m = m[0]
        elems.append(m.strip())
        srs_string = srs_string[len(m):]
    
    elems = list(map(lambda x: tuple(map(str.strip,x.split('->'))), elems))
    return elems


def translate(string_pairs:list[tuple[str, ...]]):
    
    # собираем все именаs
    names = set.union(*map(lambda x: set(x[0])|set(x[1]), string_pairs))

    elems = []
    for l,r in string_pairs:
        elems.append(
            (
                LinFunc.multicomposition(l),
                LinFunc.multicomposition(r), 
                (l,r)
            )
        )
    
    return elems, names
        
        


