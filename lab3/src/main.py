from automaton import build_simple_automaton
from regex_utils import generate_regex
from language_generation import generate_language, expand_alphabet, is_regular
from pumping import find_pumping, check_combined_pumping
import os

C = 0.99
P = 100
P_prime = 1000

Σ = set("abcdefghijklmnopqrstuvwxyz")
Φ1 = {"a"}

P_Φ1 = set()
S_Φ1 = set()

def read_tests_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def write_to_file(file_path, data):
    with open(file_path, 'a') as file:
        file.write(data + '\n')

def main():
    open('results.txt', 'w').close()

    if os.path.exists('input.txt'):
        test_files = ['input.txt']
    else:
        test_files = [f for f in os.listdir('../tests') if f.endswith('.txt')]

    for test_file in test_files:
        test_data = read_tests_from_file(os.path.join('../tests', test_file))
        L = set(test_data) 

        unique_chars = set(''.join(test_data))

        Φ = Φ1 | unique_chars

        output = f"Результаты для {test_file}:\n"

        P_Φ = generate_language(Φ, 2)
        S_Φ = generate_language(Φ, 2)

        if is_regular(P_Φ, C, P) and is_regular(S_Φ, C, P):
            output += f"Языки префиксов и суффиксов для {Φ} являются регулярными.\n"
        else:
            output += f"Языки префиксов и суффиксов для {Φ} не являются регулярными.\n"

        pumping_P = find_pumping(P_Φ)
        pumping_S = find_pumping(S_Φ)

        if check_combined_pumping(L, pumping_P, pumping_S, P_prime):
            output += f"Комбинированная накачка найдена для {Φ}.\n"
        else:
            output += f"Комбинированная накачка не найдена для {Φ}.\n"

        output += "Возможные накачки для префиксов: " + str(pumping_P) + "\n"
        output += "Возможные накачки для суффиксов: " + str(pumping_S) + "\n"

        write_to_file('results.txt', output)

if __name__ == "__main__":
    main()