from models.linear import LinFunc
from itertools import groupby
from operator import attrgetter, itemgetter


def normalize_seq(seq):
    groups = groupby(seq, key=attrgetter('degree'))
    # for k, g in groups:
        # print(k, list(g))
    
    elems = [
        '(+ ' 
            + ' '.join(map(
                lambda x: '(* ' + ' '.join(x) + ')', 
                map(attrgetter('coefs'), g))) + 
        ')'
        for _, g in groups
    ]
    return elems




def allign_seqs(seq1, seq2):
    seq1, seq2 = normalize_seq(seq1), normalize_seq(seq2)
    if len(seq2) > len(seq1):
        seq1 = ['0']*abs(len(seq2) - len(seq1)) + seq1
    else:
        seq2 = ['0']*abs(len(seq2) - len(seq1)) + seq2

    return seq1, seq2


def draw_se1_gt_seq2(seq1, seq2, s, sign, idents):
    tab = '    '

    def loop(seq1, seq2, s, sign, idents):
        s += '\n'
        if len(seq1) == 1:
            s += tab*(idents) + f'({sign} {seq1[0]} {seq2[0]})'
            return s
        s += tab*idents + '(or\n'
        s += tab*(idents+1) + f'({">"} {seq1[0]} {seq2[0]})\n'
        s += tab*(idents+1) + '(and\n'
        s += tab*(idents+2) + f'(= {seq1[0]} {seq2[0]})'
        s = loop(seq1[1:], seq2[1:], s, sign, idents+2)
        s += '))'
        return s


    return loop(seq1, seq2, s, sign, idents)
        


def create_smt(srs: list[tuple[LinFunc, LinFunc, tuple[str,str]]], names:set[str]):
    s = '(set-logic QF_NIA)\n\n'
    
    for name in names:
        for ch in 'abcd':
            s += f'(declare-fun {ch}_{name} () Int) '
            s += f'(assert (> {ch}_{name} 0))\n'
    s += '\n\n'

    for srs_elem in srs:
        lbx, lbi = srs_elem[0].by_x.elems, srs_elem[0].by_i.elems
        rbx, rbi = srs_elem[1].by_x.elems, srs_elem[1].by_i.elems

        lbx, rbx = allign_seqs(lbx, rbx)
        lbi, rbi = allign_seqs(lbi, rbi)
        print(lbx, rbx)
        print(lbi, rbi)

        s += f'; {srs_elem[2][0]} -> {srs_elem[2][1]}\n'
        s += f'; {srs_elem[0]} \n; -> {srs_elem[1]}\n'
        s += f'(assert\n'
        s += f'    (and \n'
        s += f'        (and \n'
        s += f'            ; по x нестрогое'
        s = draw_se1_gt_seq2(lbx, rbx, s, '>=',3)
        s += '\n'
        s += f'            ; по свободному члену нестрогое'
        s = draw_se1_gt_seq2(lbi, rbi, s, '>=',3)
        s += ')\n'
        s += f'        ; по кому-то из них строгое\n'
        s += f'        (or'
        s = draw_se1_gt_seq2(lbx, rbx, s, '>',3)
        s = draw_se1_gt_seq2(lbi, rbi, s, '>',3)
        s += ')))'
        s += '\n\n'

    s += '(check-sat)'
    print(s)
    return s
