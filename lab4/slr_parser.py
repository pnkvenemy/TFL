class SLRParser:
    def __init__(self, priority_direction='from_senior_to_junior'):
        self.grammar_rules = [
            ('E', ['E', '+', 'T']),
            ('E', ['T']),
            ('T', ['T', '*', 'F']),
            ('T', ['F']),
            ('F', ['(', 'E', ')']),
            ('F', ['id'])
        ]
        self.action = [
            {'id': 's5', '(': 's4'},
            {'+': 's6', '$': 'accept'},
            {'+': 'r2', '*': 's7', ')': 'r2', '$': 'r2'},
            {'+': 'r4', '*': 'r4', ')': 'r4', '$': 'r4'},
            {'id': 's5', '(': 's4'},
            {'+': 'r6', '*': 'r6', ')': 'r6', '$': 'r6'},
            {'id': 's5', '(': 's4'},
            {'id': 's5', '(': 's4'},
            {')': 's11'},
            {'+': 'r1', '*': 's7', ')': 'r1', '$': 'r1'},
            {'+': 'r3', '*': 'r3', ')': 'r3', '$': 'r3'},
            {'+': 'r5', '*': 'r5', ')': 'r5', '$': 'r5'}
        ]
        self.goto = [
            {'E': 1, 'T': 2, 'F': 3},
            {},
            {'E': 1, 'T': 2, 'F': 3},
            {},
            {'E': 8, 'T': 2, 'F': 3},
            {},
            {'T': 9, 'F': 3},
            {'F': 10},
            {},
            {},
            {},
            {}
        ]

        self.follow = {
            'E': {'$'},
            'T': {'+', '*', ')', '$'},
            'F': {'(', '$'}
        }

        self.priority_direction = priority_direction
    
    def perform_reduction(self, rule, state_stack, symbol_stack):
        
        rule_non_terminal, rule_production = rule
        rule_len = len(rule_production)

        for _ in range(rule_len):
            symbol_stack.pop()
            state_stack.pop()

        symbol_stack.append(rule_non_terminal)

        current_state = state_stack[-1]
        next_state = self.goto[current_state].get(rule_non_terminal)
        if next_state is not None:
            state_stack.append(next_state)
        else:
            raise Exception("Ошибка свертки: нет перехода в GOTO таблице")

    def parse(self, tokens, test_number):
        # tokens = self.tokenize_input(tokens) + [('$', -1, -1)]
        tokens = [(tok, line, pos) for line, line_content in enumerate(tokens.split('\n')) 
                  for pos, tok in enumerate(line_content.split())] + [('$', -1, -1)]      
        state_stack = [0]
        symbol_stack = []
        parse_steps = []
        panic_mode = False
        error_positions = []
      
        for token, line, pos in tokens:
            state = state_stack[-1]
            token, line, pos = tokens[0]
            action = self.action[state].get(token)

            if action is None:
                if not panic_mode:
                    panic_mode = True
                    parse_steps.append(f"Test {test_number}: ----- Ошибка: неожиданный символ '{token}' в строке {line}, позиция {pos}. Вход в режим паники.")
                    error_positions.append((line, pos))
                panic_mode = self.handle_error(tokens, state_stack, symbol_stack, parse_steps, line, pos)
                continue

            if symbol_stack and symbol_stack[-1] in self.grammar_rules and token in self.follow[symbol_stack[-1]]:
                panic_mode = False
                continue

            if panic_mode:
                panic_mode = False
                parse_steps.append(f"----- Восстановление после ошибки при обработке '{token}'.")
                continue

            if action == 'accept':
                parse_steps.append("============ Успешный разбор ============")
                break

            if action.startswith('s'):
                symbol_stack.append(token)
                state_stack.append(int(action[1:]))
                parse_steps.append(f"Test {test_number}: Сдвиг: Символ '{token}', Состояние {state_stack}")
                tokens.pop(0)
            elif action.startswith('r'):
                rule_number = int(action[1:]) - 1
                rule = self.grammar_rules[rule_number]
                rule_len = len(rule[1])

                for _ in range(rule_len):
                    symbol_stack.pop()
                    state_stack.pop()

                state = state_stack[-1]
                symbol_stack.append(rule[0])
                state_stack.append(self.goto[state].get(rule[0]))
                parse_steps.append(f"Test {test_number}: Свертка: Правило '{rule[0]} -> {' '.join(rule[1])}', Состояние {state_stack}")

            if action.startswith('r'):
                rule_number = int(action[1:]) - 1
                rule = self.grammar_rules[rule_number]

                applicable_rules = self.determine_rule_priority([rule])
                selected_rule = applicable_rules[0]
                self.perform_reduction(selected_rule, state_stack, symbol_stack)


        if panic_mode:
            parse_steps.append("============ Неуспешный разбор ============")
            for line, pos in error_positions:
                parse_steps.append(f"Ошибка в строке {line}, позиция {pos}")
        elif not error_positions:
            parse_steps.append("============ Успешный разбор ============")
        
        return parse_steps
    
    def determine_rule_priority(self, rules):
        if self.priority_direction == 'from_senior_to_junior':
            return sorted(rules, key=lambda r: (-self.get_seniority_level(r[0]), -len(r[1])))
        else:
            return sorted(rules, key=lambda r: (self.get_seniority_level(r[0]), len(r[1])))

    def get_seniority_level(self, non_terminal):
        seniority = {'E': 2, 'T': 1, 'F': 0}
        return seniority.get(non_terminal, -1)

    def tokenize_input(self, input_string):
        tokens = []
        for line, line_content in enumerate(input_string.split('\n')):
            for pos, tok in enumerate(line_content.split()):
                tokens.append((self.map_token(tok), line, pos))
        return tokens


    def handle_error(self, tokens, state_stack, symbol_stack, parse_steps, line, pos):
        current_non_terminal = symbol_stack[-1] if symbol_stack else None
        sync_tokens = self.follow.get(current_non_terminal, set())

        parse_steps.append(f"----- Ошибка: неожиданный символ '{tokens[0][0]}' в строке {line}, позиция {pos}. Вход в режим паники.")
        while tokens:
            token, _, _ = tokens[0]
            if token in sync_tokens or token == '$':
                break
            tokens.pop(0)

        return True if tokens else False