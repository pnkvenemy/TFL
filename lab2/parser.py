CONCAT_OP = '·'
INTERSECT_OP = '∩'

def lexer(regex):
    lexemes = []
    balance = 0
    escaped = False

    for char in regex:
        if escaped:
            lexemes.append((char, "TERM"))
            escaped = False
        elif char == '\\':
            escaped = True
        elif char == '^':
            lexemes.append(("^", "START-LINE"))
        elif char in "()":
            lexemes.append((char, "BRACKET"))
            balance += 1 if char == '(' else -1
        elif char == '$':
            lexemes.append((char, "END-LINE"))
        elif char == '|':
            lexemes.append((char, "BINARY"))
        elif char in '*+?':
            lexemes.append((char, "UNARY"))
        else:
            lexemes.append((char, "TERM"))

        if balance < 0:
            raise ValueError("Неправильный баланс скобок в регулярном выражении")

    if balance != 0:
        raise ValueError("Неправильный баланс скобок в регулярном выражении")

    return lexemes

def to_postfix(lexemes):
    output = []
    stack = []

    priority = {'|': 1, '·': 2, '*': 3, '+': 3, '?': 3}

    for lexeme in lexemes:
        if lexeme[1] == "TERM" or lexeme[1] == "START-LINE" or lexeme[1] == "END-LINE":
            output.append(lexeme)
        elif lexeme[0] == '(':
            stack.append(lexeme)
        elif lexeme[0] == ')':
            while stack and stack[-1][0] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and priority.get(lexeme[0], 0) <= priority.get(stack[-1][0], 0):
                output.append(stack.pop())
            stack.append(lexeme)

    while stack:
        output.append(stack.pop())

    return output

def get_priority(op):
    priorities = {'|': 1, CONCAT_OP: 2, '*': 3, INTERSECT_OP: 4}
    return priorities.get(op, 0)
def replace_lookbehind(lexemes, pos):
    balance = 1
    start_line_flag = False
    if lexemes[pos + 1][0] == "^":
        start_line_flag = True
    lexemes.pop(pos)
    if start_line_flag:
        lexemes.pop(pos)
    for i in range(pos, len(lexemes)):
        if lexemes[i][0] == "(":
            balance += 1
        elif lexemes[i][0] == ")":
            balance -= 1
            if balance == 0:
                lexemes.insert(i + 1, (")", "BRACKET"))
                break

    lexemes.insert(pos, (INTERSECT_OP, "INTERSECT"))
    if not start_line_flag:
        lexemes.insert(pos + 1, (".", "DOT"))
        lexemes.insert(pos + 2, ("*", "UNARY"))
        lexemes.insert(pos + 3, (CONCAT_OP, "CONCAT"))

    return lexemes

def replace_lookahead(lexemes, pos):
    balance = 1
    end_line_flag = False
    lexemes.insert(pos, ("(", "BRACKET"))
    lexemes.pop(pos + 1)

    for i in range(pos + 1, len(lexemes)):
        if lexemes[i][0] == "(":
            balance += 1
        elif lexemes[i][0] == ")":
            balance -= 1
            if balance == 0:
                if lexemes[i - 1][1] == "END-LINE":
                    end_line_flag = True
                    lexemes.pop(i - 1)
                lexemes.pop(i)
                break

    if not end_line_flag:
        lexemes.insert(i, (CONCAT_OP, "CONCAT"))
        lexemes.insert(i + 1, (".", "DOT"))
        lexemes.insert(i + 2, ("*", "UNARY"))
    lexemes.insert(i + 3, (INTERSECT_OP, "INTERSECT"))

    return lexemes

# Пример использования
regex = "abc(?=def)"
lexemes = lexer(regex)
lexemes = replace_lookahead(lexemes, 2)
print("Lexemes with lookahead:", lexemes)

# Пример использования
regex = "(?<=abc)def"
lexemes = lexer(regex)
lexemes = replace_lookbehind(lexemes, 0)
print("Lexemes with lookbehind:", lexemes)

# Пример использования
regex = "(a|b)*abb"
lexemes = lexer(regex)
postfix = to_postfix(lexemes)
print("Postfix:", postfix)
