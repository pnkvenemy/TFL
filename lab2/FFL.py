class FFL:
    def __init__(self, term=None):
        self.First = set()
        self.Follow = {}
        self.Last = set()
        self.flag = 0

        if term is not None:
            # Проверка, что term является кортежем и второй элемент - "TERM"
            assert isinstance(term, tuple) and term[1] == "TERM"
            self.First.add(term[0])
            self.Last.add(term[0])
            self.Follow[term[0]] = set()

    def concatenate(self, b):
        # Проверка валидности входного объекта
        if not isinstance(b, FFL):
            raise ValueError("Объект для конкатенации должен быть экземпляром FFL")

        for elem in self.Last:
            self.Follow[elem].update(b.First)

        # Обновление множества Last в зависимости от значения flag
        if b.flag == 0:  # b не принимает пустое слово
            self.Last = b.Last
        else:
            self.Last.update(b.Last)

        # Обновление множества First и флага
        if self.flag:
            self.First.update(b.First)
        self.flag = self.flag and b.flag

    def alternative(self, b):
        # Проверка валидности входного объекта
        if not isinstance(b, FFL):
            raise ValueError("Объект для альтернативы должен быть экземпляром FFL")

        self.First.update(b.First)
        self.Last.update(b.Last)
        self.flag = self.flag or b.flag

        # Объединение Follow множеств
        for key, value in b.Follow.items():
            if key in self.Follow:
                self.Follow[key].update(value)
            else:
                self.Follow[key] = value

    def unary(self, operator="*"):
        # Поддержка различных унарных операторов
        if operator == "*":
            # Клини звезда: элемент может повторяться ноль или более раз
            for elem in self.Last:
                self.Follow[elem].update(self.First)
            self.flag = True
        elif operator == "+":
            # Унарный плюс: элемент должен повторяться один или более раз
            for elem in self.Last:
                self.Follow[elem].update(self.First)
            # Флаг остается без изменений, так как "+" требует хотя бы одного вхождения
        elif operator == "?":
            # Знак вопроса: элемент может быть, а может и не быть
            # Не требует изменений в Follow множестве
            self.flag = True
        else:
            raise ValueError("Неизвестный унарный оператор")
