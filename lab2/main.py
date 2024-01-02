import os

from parser import lexer, to_postfix  
from tree import construct_expression_tree  
from ts import StateMachine  
from regex_generator import generate_random_regex
from string_generator import generate_string_from_state_machine
from regex_comparison import compare_parsing
from fuzz_module import FuzzTester

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

def generate_and_test_string(regex):
    lexemes = lexer(regex)
    postfix = to_postfix(lexemes)
    expression_tree = construct_expression_tree(postfix)
    state_machine = StateMachine([0], [[]], [False])
    state_machine.convert_tree_to_state_machine(expression_tree)
    state_machine.remove_dead_ends()

    generated_string = generate_string_from_state_machine(state_machine)
    python_result, our_result = compare_parsing(regex, generated_string)

    print(f"Генерация строк: {generated_string}")
    print(f"результат пай: {python_result}, результат our: {our_result}")


def main():
    for _ in range(10):

        random_regex = generate_random_regex()

        lexemes = lexer(random_regex)
        postfix = to_postfix(lexemes)
        expression_tree = construct_expression_tree(postfix)

        state_machine = StateMachine([0], [[]], [False])
        state_machine.convert_tree_to_state_machine(expression_tree)
        state_machine.remove_dead_ends()
        test_string = generate_string_from_state_machine(state_machine)
        python_result, our_result = compare_parsing(random_regex, test_string)
        FuzzTester()

        print(f"Regex: {random_regex}")
        print(f"Test String: {test_string}")
        print(f"Python Result: {python_result}, Our Result: {our_result}")

        input_data = read_input_file('input.txt')
        if input_data:
            processed_data = process_data(input_data)
            print(processed_data)  
        else:
            run_tests()

if __name__ == "__main__":
    main()