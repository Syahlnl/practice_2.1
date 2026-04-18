def process_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                for line in input_file:
                    numbers = line.strip().split()

                    for num_str in numbers:
                        try:
                            num = int(num_str)

                            if num % 7 == 0:
                                denominator = 73 ** 2 + 29
                                result = num * 100 / denominator
                                output_file.write(f"{result:.6f}\n")
                                print(f"Число {num} обработано")

                        except ValueError:
                            continue

        print(f"\nРезультаты сохранены в {output_filename}")
        return True

    except FileNotFoundError:
        print("Ошибка: входной файл не найден")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def create_sample_file(filename="numbers.txt"):
    sample_numbers = [7, 14, 21, 28, 35, 42, 49, 56, 63, 70]

    with open(filename, 'w', encoding='utf-8') as file:
        for i in range(0, len(sample_numbers), 3):
            line = " ".join(str(num) for num in sample_numbers[i:i + 3])
            file.write(line + "\n")

    print(f"Создан пример файла {filename}")
    print("Содержимое файла:")
    with open(filename, 'r', encoding='utf-8') as file:
        print(file.read())


def main():
    print("ПОИСК ЧИСЕЛ, КРАТНЫХ 7")

    input_file = input("Введите имя входного файла: ").strip()
    if not input_file:
        input_file = "numbers.txt"

    output_file = input("Введите имя выходного файла: ").strip()
    if not output_file:
        output_file = "result.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as test_file:
            pass
    except FileNotFoundError:
        print(f"Файл {input_file} не найден")
        create = input("Создать пример файла? (да/нет): ").strip().lower()
        if create in ['да', 'yes', 'д']:
            create_sample_file(input_file)
        else:
            return

    denominator = 73 ** 2 + 29
    print(f"\nЗнаменатель: 73² + 29 = {denominator}")
    print("Операция: x * 100 / (73² + 29)")

    process_file(input_file, output_file)


if __name__ == "__main__":
    main()