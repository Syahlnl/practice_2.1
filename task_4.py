import math
import datetime


def show_last_operations(log_file="resource/calculator.log"):
    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if not lines:
            print("Лог-файл пуст")
            return

        last_five = lines[-5:] if len(lines) >= 5 else lines

        print("Последние 5 операций:")
        for line in last_five:
            print(line.strip())

    except FileNotFoundError:
        print("Лог-файл пока не создан")


def write_to_log(operation, result, log_file="resource/calculator.log"):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(f"[{timestamp}] {operation} = {result}\n")

    except Exception:
        print("Ошибка: не удалось записать в лог-файл")


def clear_log(log_file="resource/calculator.log"):
    try:
        with open(log_file, 'w', encoding='utf-8') as file:
            file.write("")
        print("Лог-файл успешно очищен")

    except Exception:
        print("Ошибка: не удалось очистить лог-файл")


def get_number(prompt):
    try:
        return float(input(prompt))

    except ValueError:
        print("Ошибка: введите число")
        return None


def calculate():
    print("Доступные операции: +, -, *, /, log, sin")

    operation = input("Введите операцию: ").strip().lower()

    match operation:
        case '+':
            a = get_number("Введите первое число: ")
            if a is None:
                return
            b = get_number("Введите второе число: ")
            if b is None:
                return
            result = a + b
            write_to_log(f"{a} + {b}", result)
            print(f"Результат: {result}")

        case '-':
            a = get_number("Введите первое число: ")
            if a is None:
                return
            b = get_number("Введите второе число: ")
            if b is None:
                return
            result = a - b
            write_to_log(f"{a} - {b}", result)
            print(f"Результат: {result}")

        case '*':
            a = get_number("Введите первое число: ")
            if a is None:
                return
            b = get_number("Введите второе число: ")
            if b is None:
                return
            result = a * b
            write_to_log(f"{a} * {b}", result)
            print(f"Результат: {result}")

        case '/':
            a = get_number("Введите первое число: ")
            if a is None:
                return
            b = get_number("Введите второе число: ")
            if b is None:
                return
            if b == 0:
                print("Ошибка: деление на ноль")
                return
            result = a / b
            write_to_log(f"{a} / {b}", result)
            print(f"Результат: {result}")

        case 'log':
            a = get_number("Введите число: ")
            if a is None:
                return
            if a <= 0:
                print("Ошибка: логарифм определен только для положительных чисел")
                return
            result = math.log10(a)
            write_to_log(f"log({a})", result)
            print(f"Результат: {result}")

        case 'sin':
            a = get_number("Введите угол в градусах: ")
            if a is None:
                return
            result = math.sin(math.radians(a))
            write_to_log(f"sin({a}°)", result)
            print(f"Результат: {result}")

        case _:
            print("Ошибка: неизвестная операция")


def main():
    show_last_operations()

    while True:
        print("1. Выполнить операцию")
        print("2. Очистить лог-файл")
        print("3. Выйти")

        choice = input("Выберите действие (1-3): ").strip()

        match choice:
            case '1':
                calculate()
            case '2':
                clear_log()
            case '3':
                print("До свидания!")
                break
            case _:
                print("Ошибка: выберите действие от 1 до 3")


if __name__ == "__main__":
    main()