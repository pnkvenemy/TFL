import os
def read_from_file( file_path):
        with open(file_path, 'r') as file:
            return file.read()
        
def map_token(self, token):
        if token == ' ':
            return '_'
        elif token == '\n':
            return '$'
        else:
            return token
        
def read_test_cases(tests_folder):
    test_cases = []
    for test_file in os.listdir(tests_folder):
        if test_file.startswith("test"):
            with open(os.path.join(tests_folder, test_file), 'r') as file:
                test_cases.append(file.read())
    return test_cases
def write_output(output_file, output_data):
    with open(output_file, 'w') as file:
        file.write(output_data)