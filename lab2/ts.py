class StateMachine:
    def __init__(self, initial_states, transitions, end_states):
        self.initial_states = initial_states
        self.transitions = transitions
        self.end_states = end_states

    def minimize_states(self):
      
        dfa = self.convert_to_dfa()      
        groups = dfa.initial_grouping()

        while True:
            new_groups = dfa.refine_groups(groups)
            if new_groups == groups:
                break
            groups = new_groups

        minimized_dfa = dfa.create_minimized_dfa(groups)
        self.update_to_minimized(minimized_dfa)

    def convert_to_dfa(self):
        dfa_states = {frozenset([self.initial_state])}
        dfa_transitions = {}
        dfa_final_states = set()

        queue = [frozenset([self.initial_state])]
        while queue:
            current = queue.pop(0)
            for symbol in self.alphabet:
                next_states = frozenset({s for state in current for s in self.transitions.get((state, symbol), set())})
                dfa_transitions[(current, symbol)] = next_states
                if next_states not in dfa_states:
                    dfa_states.add(next_states)
                    queue.append(next_states)
                if not dfa_final_states.intersection(next_states) and next_states.intersection(self.final_states):
                    dfa_final_states.add(next_states)

    def initial_grouping(self):
        final_states = {state for state in self.states if state in self.final_states}
        non_final_states = self.states - final_states
        return [final_states, non_final_states]

    def refine_groups(self, groups):
        new_groups = []
        for group in groups:
            subgroups = {}
            for state in group:
                key = tuple(self.transitions.get((state, symbol)) for symbol in self.alphabet)
                subgroups.setdefault(key, set()).add(state)
            new_groups.extend(subgroups.values())
        return new_groups

    def create_minimized_dfa(self, groups):
        new_states = {frozenset(group) for group in groups}
        new_transitions = {}
        new_initial_state = frozenset({self.initial_state})
        new_final_states = {frozenset(group) for group in groups if self.final_states.intersection(group)}

        for group in groups:
            representative = next(iter(group))
            for symbol in self.alphabet:
                next_state = self.transitions.get((representative, symbol))
                if next_state:
                    new_transitions[(frozenset(group), symbol)] = frozenset(next_state)

    def update_to_minimized(self, minimized_dfa):
        self.states = minimized_dfa.states
        self.transitions = minimized_dfa.transitions
        self.initial_state = minimized_dfa.initial_state
        self.final_states = minimized_dfa.final_states

    def get_initial_states(self):
        return self.initial_states

    def get_transitions(self):
        return self.transitions

    def get_final_states(self):
        return self.end_states

    def display(self):
        print("Initial States:", self.initial_states)
        print("Transition Matrix:")
        for transition in self.transitions:
            print(transition)
        print("Final States:", self.final_states)

    def depth_first_search(self, node, seen=None):
        if seen is None:
            seen = [False] * len(self.transitions)
        seen[node] = True
        for index, connection in enumerate(self.transitions[node]):
            if connection != "0" and not seen[index]:
                self.depth_first_search(index, seen)

    def remove_dead_ends(self):
        accessible = [False] * len(self.transitions)
        for start in self.initial_states:
            self.depth_first_search(start, accessible)

        self.transitions = [row for idx, row in enumerate(self.transitions) if accessible[idx]]
        self.initial_states = [state for idx, state in enumerate(self.initial_states) if accessible[idx]]
        self.end_states = [state for idx, state in enumerate(self.end_states) if accessible[idx]]  


    def convert_to_regex(self):
        states_count = len(self.transitions)

        regex_matrix = [["" for _ in range(states_count)] for _ in range(states_count)]

        for i in range(states_count):
            for j in range(states_count):
                if self.transitions[i][j] != "0":
                    regex_matrix[i][j] = self.transitions[i][j]
                if i == j:
                    regex_matrix[i][j] += "ε"

        for k in range(states_count):
            for i in range(states_count):
                for j in range(states_count):
                    regex_matrix[i][j] = self.or_regex(
                        regex_matrix[i][j],
                        self.concat_regex(regex_matrix[i][k], self.concat_regex(self.star_regex(regex_matrix[k][k]), regex_matrix[k][j]))
                    )

        final_regex = ""
        for end_state in self.end_states: 
            final_regex = self.or_regex(final_regex, regex_matrix[0][end_state])

        return final_regex if final_regex else "ε"

    @staticmethod
    def concat_regex(r1, r2):
        if r1 == "ε":
            return r2
        if r2 == "ε":
            return r1
        return f"({r1})({r2})" if r1 and r2 else r1 or r2

    @staticmethod
    def or_regex(r1, r2):
        if not r1 or r1 == "ε":
            return r2
        if not r2 or r2 == "ε":
            return r1
        if r1 == r2: 
            return r1
        return f"({r1}|{r2})"

    @staticmethod
    def star_regex(r):
        if not r or r == "ε" or r.endswith("*"):
            return r
        return f"({r})*"

    def simplify_regex(self, regex):
        simplified = regex.replace("(ε)", "") 
        simplified = simplified.replace("ε|", "")  
        simplified = simplified.replace("|ε", "")

        pattern = re.compile(r'\(([^)]+)\|\1\)')
        while pattern.search(simplified):
            simplified = pattern.sub(r'(\1)', simplified)

        pattern = re.compile(r'\(([^)]+)\)\*\|\(\)')
        while pattern.search(simplified):
            simplified = pattern.sub(r'(\1)*', simplified)

        return simplified

        return simplified_regex

    def ensure_matrix_size(self, size):
        while len(self.transitions) <= size:
            self.transitions.append(["0"] * (size + 1))

        for row in self.transitions:
            while len(row) <= size:
                row.append("0")

    def convert_tree_to_state_machine(self, node, current_state=0):
        if node is None:
            return current_state

        if node.value[1] == "TERM":
            next_state = len(self.transitions)
            self.ensure_matrix_size(next_state)
            self.transitions[current_state][next_state] = node.value[0]
            return next_state

        elif node.value[1] == "BINARY":
            left_state = self.convert_tree_to_state_machine(node.left_node, current_state)
            right_state = self.convert_tree_to_state_machine(node.right_node, current_state)

            if node.value[0] == "|":
                new_state = len(self.transitions)
                self.ensure_matrix_size(new_state)
                self.transitions[current_state][left_state] = "eps"
                self.transitions[current_state][right_state] = "eps"
                return new_state
            elif node.value[0] == ".":
                return self.convert_tree_to_state_machine(node.right_node, left_state)

        elif node.value[1] == "UNARY" and node.value[0] == "*":
            next_state = len(self.transitions)
            self.ensure_matrix_size(next_state)
            self.transitions[current_state][next_state] = "eps"
            self.transitions[next_state][next_state] = node.left_node.value[0]
            self.transitions[next_state][current_state] = "eps"
            return next_state

        return current_state
    def check_word(self, word):

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