from slr_parser import SLRParser
from utils import read_test_cases, write_output
import os

if __name__ == "__main__":
    slr_parser = SLRParser()
    input_file_path = "input"
    output_file_path = "output"
    tests_folder = "tests"

    if os.path.exists(input_file_path) and os.path.getsize(input_file_path) == 0:
        test_cases = read_test_cases(tests_folder)
        all_output = ""
        test_number = 1

        for input_string in test_cases:
            parse_steps = slr_parser.parse(input_string, test_number)
            all_output += "\n".join(parse_steps) + "\n\n"
            test_number += 1

        write_output(output_file_path, all_output)
    elif os.path.exists(input_file_path):
        with open(input_file_path, 'r') as file:
            input_string = file.read()
        
        parse_steps = slr_parser.parse(input_string, 1)
        print("============= SLR(1)-разбор слова ============")
        for step in parse_steps:
            print(step)
    else:
        print(f"Файл '{input_file_path}' не найден.")
