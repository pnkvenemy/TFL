class Automaton:
    def __init__(self, start_states, transition_matrix, end_states):
        self.start_states = start_states
        self.transition_matrix = transition_matrix
        self.end_states = end_states

    def get_start_states(self):
        return self.start_states

    def get_transition_matrix(self):
        return self.transition_matrix

    def get_end_states(self):
        return self.end_states

    def show_automaton(self):
        print("Start States:", self.start_states)
        print("Transition Matrix:")
        for row in self.transition_matrix:
            print(row)
        print("End States:", self.end_states)

    def dfs(self, vertex, visited=None):
        # Поиск в глубину для обхода автомата.
        if visited is None:
            visited = [False] * len(self.transition_matrix)
        visited[vertex] = True
        for i, edge in enumerate(self.transition_matrix[vertex]):
            if edge != "0" and not visited[i]:
                self.dfs(i, visited)

    def delete_traps(self):
        # Удаление ловушечных состояний из автомата.
        reachable = [False] * len(self.transition_matrix)
        for start in self.start_states:
            self.dfs(start, reachable)

        # Удаление недостижимых состояний
        self.transition_matrix = [row for i, row in enumerate(self.transition_matrix) if reachable[i]]
        self.start_states = [state for i, state in enumerate(self.start_states) if reachable[i]]
        self.end_states = [state for i, state in enumerate(self.end_states) if reachable[i]]

    def automaton_to_regex(self):
        states_count = len(self.transition_matrix)
        regex_matrix = [["" for _ in range(states_count)] for _ in range(states_count)]

        # Инициализация регулярных выражений для переходов
        for i in range(states_count):
            for j in range(states_count):
                if self.transition_matrix[i][j] != "0":
                    regex_matrix[i][j] = self.transition_matrix[i][j]
                if i == j:
                    regex_matrix[i][j] += "ε"

        # Применяем алгоритм преобразования
        for k in range(states_count):
            for i in range(states_count):
                for j in range(states_count):
                    regex_matrix[i][j] = self.or_regex(
                        regex_matrix[i][j],
                        self.concat_regex(regex_matrix[i][k], self.concat_regex(self.star_regex(regex_matrix[k][k]), regex_matrix[k][j]))
                    )

        # Формируем конечное регулярное выражение
        final_regex = ""
        for end_state in self.end_states:
            final_regex = self.or_regex(final_regex, regex_matrix[0][end_state])

        return final_regex if final_regex else "ε"

    @staticmethod
    def concat_regex(r1, r2):
        # Упрощаем конкатенацию с учётом ε
        if r1 == "ε":
            return r2
        if r2 == "ε":
            return r1
        return f"({r1})({r2})" if r1 and r2 else r1 or r2

    @staticmethod
    def or_regex(r1, r2):
        # Упрощаем альтернативу
        if not r1 or r1 == "ε":
            return r2
        if not r2 or r2 == "ε":
            return r1
        if r1 == r2:  # Удаляем дубликаты
            return r1
        return f"({r1}|{r2})"

    @staticmethod
    def star_regex(r):
        # Упрощаем звёздочку Клини
        if not r or r == "ε" or r.endswith("*"):
            return r
        return f"({r})*"

    # Дополнительный метод для упрощения выражений
    def simplify_regex(self, regex):
        # Удаляем избыточные скобки и ε, применяем другие упрощения
        simplified = regex.replace("(ε)", "")  # Удаляем (ε)
        simplified = simplified.replace("ε|", "")  # Удаляем ε| и |ε
        simplified = simplified.replace("|ε", "")

        # Удаление дубликатов в альтернативах: например, (a|a) становится (a)
        pattern = re.compile(r'\(([^)]+)\|\1\)')
        while pattern.search(simplified):
            simplified = pattern.sub(r'(\1)', simplified)

        # Упрощение случаев типа (a)*|() в a*
        pattern = re.compile(r'\(([^)]+)\)\*\|\(\)')
        while pattern.search(simplified):
            simplified = pattern.sub(r'(\1)*', simplified)

        return simplified

        return simplified_regex
    def ensure_matrix_size(self, size):
        while len(self.transition_matrix) <= size:
            self.transition_matrix.append(["0"] * (size + 1))

        for row in self.transition_matrix:
            while len(row) <= size:
                row.append("0")

    def convert_tree_to_automaton(self, node, current_state=0):
        if node is None:
            return current_state

        if node.data[1] == "TERM":
            next_state = len(self.transition_matrix)
            self.ensure_matrix_size(next_state)
            self.transition_matrix[current_state][next_state] = node.data[0]
            return next_state

        elif node.data[1] == "BINARY":
            if node.data[0] == "|":
                left_state = self.convert_tree_to_automaton(node.left, current_state)
                right_state = self.convert_tree_to_automaton(node.right, current_state)
                return max(left_state, right_state)
            elif node.data[0] == ".":
                left_state = self.convert_tree_to_automaton(node.left, current_state)
                return self.convert_tree_to_automaton(node.right, left_state)

        elif node.data[1] == "UNARY" and node.data[0] == "*":
            next_state = len(self.transition_matrix)
            self.ensure_matrix_size(next_state)
            self.transition_matrix[current_state][next_state] = "eps"
            self.transition_matrix[next_state][next_state] = node.left.data[0]
            self.transition_matrix[next_state][current_state] = "eps"
            return next_state

        return current_state
    def check_word(self, word):

        #Проверяет, принадлежит ли слово языку, заданному этим автоматом.

        current_states = set(self.start_states)

        for char in word:
            next_states = set()
            for state in current_states:
                for next_state, transition in enumerate(self.transition_matrix[state]):
                    if transition == char:
                        next_states.add(next_state)

            current_states = next_states

            if not current_states:
                return False

        return any(state in self.end_states for state in current_states)