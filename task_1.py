def create_file():
    content = ("""привет друг 
давай
вместе с тобой
изучать
python""")

    with open('resource/text.txt', 'w', encoding='utf-8') as file:
        file.write(content)

    print("\n1. Файл text.txt успешно создан\n")


def count_lines():
    try:
        with open('resource/text.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            line_count = len(lines)

        print(f"2.1. Количество строк в файле text.txt: {line_count}")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")

    except Exception as error:
        print(f"Ошибка: {error}")


def count_words():
    try:
        with open('resource/text.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            words = content.split()
            words_count = len(words)

        print(f"2.2. Количество слов в файле text.txt: {words_count}")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")

    except Exception as error:
        print(f"Ошибка: {error}")


def biggest_line():
    try:
        with open('resource/text.txt', 'r', encoding='utf-8') as file:
            content = file.readlines()
            line = max(content, key=len)

        print(f"2.3. Самая длинная строка в файле text.txt: {line}")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")

    except Exception as error:
        print(f"Ошибка: {error}")


def count_vowels_and_consonants():
    try:
        with open('resource/text.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            vowels = 'аеёиоуыэюя'
            consonants = 'бвгджзйклмнпрстфхцчшщ'
            vowels_count = 0
            consonants_count = 0

            for char in content:
                if char in vowels:
                    vowels_count += 1
                elif char in consonants:
                    consonants_count += 1

        print(f"3.1. Количество гласных в файле text.txt: {vowels_count}")

        print(f"3.2. Количество согласных в файле text.tx t: {consonants_count}")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")

    except Exception as error:
        print(f"Ошибка: {error}")


if __name__ == '__main__':
    (create_file(),count_lines(),
     count_words(),biggest_line(),count_vowels_and_consonants())