class FFL:
    def __init__(self, term=None):
        self.First = set()
        self.Follow = {}
        self.Last = set()
        self.flag = 0

        if term is not None:
            assert isinstance(term, tuple) and term[1] == "TERM"
            self.First.add(term[0])
            self.Last.add(term[0])
            self.Follow[term[0]] = set()

    def concatenate(self, b):
        for elem in self.Last:
            self.Follow[elem].update(b.First)

        if b.flag == 0:  # b не принимает пустое слово
            self.Last = b.Last
        else:
            self.Last.update(b.Last)

        if self.flag:
            self.First.update(b.First)

        self.flag = self.flag and b.flag

    def alternative(self, b):
        self.First.update(b.First)
        self.Last.update(b.Last)
        self.flag = self.flag or b.flag

        for key, value in b.Follow.items():
            if key in self.Follow:
                self.Follow[key].update(value)
            else:
                self.Follow[key] = value

    def unary(self):
        for elem in self.Last:
            self.Follow[elem].update(self.First)
        self.flag = True