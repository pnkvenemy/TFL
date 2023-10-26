from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass


def normalize_seq(seq: list[Ordinal]):
    if not seq:
        return seq
    # справа налево они только возрастают
    new_seq = [seq[-1]]
    for x in seq[::-1][1:]:
        if x.degree >= new_seq[0].degree:
            new_seq.insert(0, x)
        else:
            pass
    return new_seq


@dataclass
class Ordinal:
    degree: int
    coefs: list[str]

    def __repr__(self) -> str:
        if self.degree >= 2:
            return f'w^{self.degree}*({"*".join(self.coefs)})'
        if self.degree == 1:
            return f'w*({"*".join(self.coefs)})'
        return f'({"*".join(self.coefs)})'

    def __mul__(self, o: Ordinal):
        if o.degree == 0:
            return Ordinal(
                degree=self.degree,
                coefs=deepcopy(self.coefs) + deepcopy(o.coefs),
            )

        return Ordinal(
            degree=self.degree + o.degree,
            coefs=deepcopy(o.coefs),
        )


@dataclass
class OrdinalsSum:

    elems: list[Ordinal]

    def __init__(self, seq):
        self.elems = normalize_seq(seq)

    def __repr__(self) -> str:
        return f'({" + ".join(map(repr, self.elems))})'

    def __add__(self, o: OrdinalsSum) -> OrdinalsSum:
        return OrdinalsSum(self.elems + o.elems)

    def __mul__(self, o: OrdinalsSum) -> OrdinalsSum:
        if (o.elems) == 0:
            return OrdinalsSum([])

        # (w**a*b + c) * (w**x*y + z) == w**(a + x)*y + (c*z + (w**a*b + c)*z)
        # (x + y) * (z + w) == x*z + y*w + (x + y)*w

        # мы - то знаем, в каком месте это будет использоваться:
        # self - это всегда wa+b :))
        # o всегда имеет свободный член - можно доказать по индукции (наверное)
        x, y = self.elems[0], self.elems[1]
        z, w = deepcopy(o.elems[0]), o.elems[1:]

        if w:
            res = OrdinalsSum([x*z])
            for ww in w:
                res = res + OrdinalsSum([y*ww])
            res = res + self*OrdinalsSum(w)
            return res

        # понятия не имею, откуда тут игрек
        # https://theory.stanford.edu/~tingz/talks/ordinal.pdf - отсюда не понятно
        # https://github.com/ajcr/transfinite/blob/master/transfinite/ordinal.py - отсюда - очевидно
        return OrdinalsSum([x*z, y])


@dataclass
class LinFunc:
    by_x: OrdinalsSum
    by_i: OrdinalsSum

    def __repr__(self) -> str:
        return f'{self.by_x}*x + {self.by_i}'

    @staticmethod
    def starting(char: str):
        return LinFunc(
            by_x=OrdinalsSum(
                [Ordinal(1, [f'a_{char}']), Ordinal(0, [f'b_{char}'])]),
            by_i=OrdinalsSum(
                [Ordinal(1, [f'c_{char}']), Ordinal(0, [f'd_{char}'])]),
        )

    @staticmethod
    def composition(char: str, lf2: LinFunc):
        '''
        (w*a + b)[S1*x + S2] + w*c + d,
        где S1 и S2 - ординалы в канонической форме:
        S = sum_1^n w^a_i*b_i, a_i >= a_{i+1}
        '''
        lf1 = LinFunc.starting(char)

        '''
        раскрываем по дистрибутивности слева
        (w*a + b)[S1*x + S2] + w*c + d = 
            = (w*a + b)[S1*x] + (w*a + b)[S2] + w*c + d
            = [(w*a + b)*S1]*x + [(w*a + b)[S2] + w*c + d]
        '''

        new_by_x = lf1.by_x * lf2.by_x
        new_by_i = lf1.by_x * lf2.by_i + lf1.by_i

        return LinFunc(new_by_x, new_by_i)

    @staticmethod
    def multicomposition(chars: str):
        def loop(chars: str, lf: LinFunc):
            if not chars:
                return lf
            return loop(
                chars=chars[:-1],
                lf=LinFunc.composition(chars[-1], lf),
            )
        return loop(chars[:-1], LinFunc.starting(chars[-1]))


if __name__ == '__main__':
    print(LinFunc.composition('f', LinFunc.starting('g')))
