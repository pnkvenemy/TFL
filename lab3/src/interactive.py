
from automaton import build_simple_automaton
from regex_utils import generate_regex
from language_generation import generate_language, expand_alphabet, is_regular
from pumping import find_pumping, check_combined_pumping

def interactive_mode():
    while True:
        print("\nВыберите опцию:")
        print("1. Генерация языка")
        print("2. Построение автомата")
        print("3. Создание регулярного выражения")
        print("4. Выход")

        choice = input("Введите выбор: ")
        if choice == '4':
            break

        if choice == '1':
            alphabet = input("Введите алфавит (буквы через запятую): ").split(',')
            length = int(input("Введите длину слов: "))
            language = generate_language(set(alphabet), length)
            print("Сгенерированный язык:", language)

        elif choice == '2':
            symbols = input("Введите символы для автомата (через запятую): ").split(',')
            automaton = build_simple_automaton(set(symbols))
            print("Автомат:", automaton)

        elif choice == '3':
            words = input("Введите слова для регулярного выражения (через запятую): ").split(',')
            regex = generate_regex(words)
            print("Регулярное выражение:", regex)

if __name__ == "__main__":
    interactive_mode()
