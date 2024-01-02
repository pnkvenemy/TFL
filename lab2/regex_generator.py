import random

def generate_random_regex(pattern_length=5, include_shuffle=False, include_lookahead=False):
    symbols = "abcdefghijklmnopqrstuvwxyz"
    operators = "*+?|" 
    regex = ""
    open_parentheses = 0
    last_was_operator = False

    for _ in range(pattern_length - 1):  
        choices = symbols + operators + "()"
        if include_lookahead:
            choices += "L"  

        if last_was_operator:
            choice = random.choice(choices.replace("|", "")) 
        else:
            choice = random.choice(choices)

        if choice == "L":
            lookahead_regex = generate_random_regex(random.randint(1, 3), include_shuffle, False)
            regex += "(?=" + lookahead_regex + ")"
            continue

        if choice in operators:
            last_was_operator = True
        else:
            last_was_operator = False

        if choice == "(":
            open_parentheses += 1
        elif choice == ")":
            if open_parentheses == 0:
                continue  
            open_parentheses -= 1

        if choice in "*+?" and (len(regex) == 0 or regex[-1] in "*+?|"):
            continue

        regex += choice

    regex += ")" * open_parentheses
    if include_shuffle and random.random() < 0.2:
        regex = '[' + ''.join(random.sample(regex, len(regex))) + ']'
    return regex
