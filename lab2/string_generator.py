import random
from ts import StateMachine
def generate_string_from_state_machine(state_machine, length=10):
    """
    Генерирует строку, соответствующую регулярному выражению, представленному в виде конечного автомата.
    """
    current_state = random.choice(state_machine.get_initial_states())
    generated_string = ""

    while len(generated_string) < length:
        if current_state >= len(state_machine.get_transitions()):
            break

        transitions = state_machine.get_transitions()[current_state]
        possible_transitions = [transition for transition in transitions if transition != "0"]

        if not possible_transitions:
            break

        next_transition = random.choice(possible_transitions)
        generated_string += next_transition

        # Переход в следующее состояние
        next_state_candidates = [index for index, transition in enumerate(transitions) if transition == next_transition]
        current_state = random.choice(next_state_candidates)

    return generated_string
