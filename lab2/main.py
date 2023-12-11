import os

from parser import lexer, to_postfix
from tree import construct_expression_tree
from ts import StateMachine

def read_input_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_directory_exists('test_results')

def write_output_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

def process_data(data):
    lexemes = lexer(data)
    postfix = to_postfix(lexemes)
    expression_tree = construct_expression_tree(postfix)

    state_machine = StateMachine([0], [[]], [False])
    state_machine.convert_tree_to_state_machine(expression_tree)
    state_machine.remove_dead_ends()

    return state_machine.convert_to_regex()

def run_tests():
    test_files = os.listdir('tests')
    for test_file in test_files:
        with open(f'tests/{test_file}', 'r') as file:
            test_data = file.read().strip()
            processed_data = process_data(test_data)
            write_output_file(f'test_results/{test_file}_output.txt', processed_data)

def main():
    input_data = read_input_file('input.txt')
    if input_data:
        processed_data = process_data(input_data)
        print(processed_data)
    else:
        run_tests()

if __name__ == "__main__":
    main()