def clear_result():
    with open('resource/result.txt', 'w', encoding='utf-8') as file:
        file.write("")

def create_file():
    content = """Иванов Иван:5,4,3,5
Петров Петр:4,3,4,4
Сидорова Мария:5,5,5,5
"""

    with open('resource/students.txt', 'w', encoding='utf-8') as file:
        file.write(content)


def read_file():

    with open('resource/students.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    print(content)


def main():

    print("Средняя оценка студентов")
    best_average_score = 0
    low_average_score = 5
    try:
        with open('resource/students.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if ":" in line:
                    name, scores_str = line.split(":", 1)

                    scores = []
                    for score in scores_str.split(","):
                        try:
                            scores.append(float(score))

                        except ValueError:
                            print(f"Ошибка: Некорректная оценка: {score} у студента {name}")

                if scores:
                    average_score = sum(scores) / len(scores)
                    print(f"{name}, Средняя оценка: {average_score}")

                    if average_score > 4:
                        content = f"""{name}, Средняя оценка: {average_score}"""

                        with open('resource/result.txt', 'a', encoding='utf-8') as file:
                            file.write(content + '\n')

                    best_average_score = max(best_average_score, average_score)
                    low_average_score = min(low_average_score, average_score)

        print(f"\nСтудент с наивысшим средним баллом: {best_average_score}")
        print(f"Студент с самым низким средним баллом: {low_average_score}")

    except FileNotFoundError:
        print("Ошибка: Файл students.txt не найден")

    except Exception as e:
        print(f"Ошибка: {e}")




if __name__ == '__main__':
    clear_result(), create_file(), read_file(), main()