import re
from ts import StateMachine


def compare_parsing(regex, test_string):

    try:
        python_result = bool(re.match(regex, test_string))
    except re.error as e:
        print(f"Ошибка в регулярном выражении: {regex} - {e}")
        return None, None


    initial_states = [0]
    transitions = {
        0: { 'a': 1, 'b': 2 }, 
        1: { 'a+b': 3, 'a+b': 4 }, 
    }
    end_states = [3] 

    state_machine = StateMachine(initial_states, transitions, end_states)
    our_result = state_machine.check_word(test_string)

    return python_result, our_result
