import os

from parser import lexer, to_postfix  # Импорт функций парсера
from tree import build_tree, print_tree  # Импорт функций для работы с деревом
from ts import Automaton  # Импорт класса Automaton

def read_input_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

# Функция для записи данных в файл
# Функция для проверки существования директории и её создания при отсутствии
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Проверяем и создаем папку 'test_results', если она не существует
ensure_directory_exists('test_results')

def write_output_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)
def process_data(data):
    lexemes = lexer(data)
    postfix = to_postfix(lexemes)
    tree = build_tree(postfix)

    automaton = Automaton([0], [[]], [False])
    automaton.convert_tree_to_automaton(tree)
    automaton.delete_traps()

    return automaton.automaton_to_regex()

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
        print(processed_data)  # Вывод в стандартный поток вывода
    else:
        run_tests()  # Запуск автоматических тестов, если input.txt пуст

if __name__ == "__main__":
    main()
