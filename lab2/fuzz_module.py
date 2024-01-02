from regex_generator import generate_random_regex
from string_generator import generate_string_from_state_machine
from regex_comparison import compare_parsing
from parser import lexer, to_postfix
from tree import construct_expression_tree
from ts import StateMachine
import re
import random

class FuzzTester:

    def __init__(self, iterations=100, pattern_length=5):
        self.iterations = iterations
        self.pattern_length = pattern_length

    def run_tests(self):
        for _ in range(self.iterations):
            regex = generate_random_regex(self.pattern_length, include_shuffle=True, include_lookahead=True)
            lexemes = lexer(regex)
            postfix = to_postfix(lexemes)
            expression_tree = construct_expression_tree(postfix)
            state_machine = StateMachine([0], [[]], [False])
            state_machine.convert_tree_to_state_machine(expression_tree)
            state_machine.remove_dead_ends()

            test_string = generate_string_from_state_machine(state_machine)
            python_result = self.test_with_python(regex, test_string)
            our_result = state_machine.check_word(test_string)

            print(f"Regex: {regex}")
            print(f"Test String: {test_string}")
            print(f"результат пай: {python_result}, результат our: {our_result}")

    @staticmethod
    def test_with_python(regex, test_string):
        try:
            return bool(re.match(regex, test_string))
        except re.error:
            return None

if __name__ == "__main__":
    fuzz_tester = FuzzTester()
    fuzz_tester.run_tests()
