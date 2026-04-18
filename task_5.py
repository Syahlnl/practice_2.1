import json

FILE_NAME = 'resource/library.json'


def load_books():
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Ошибка: файл library.json не найден")
        return []
    except json.JSONDecodeError:
        print("Ошибка: файл library.json поврежден")
        return []


def save_books(books):
    try:
        with open(FILE_NAME, 'w', encoding='utf-8') as file:
            json.dump(books, file, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены")
        return True
    except Exception:
        print("Ошибка: не удалось сохранить данные")
        return False


def create_library_file():
    default_books = [
        {
            "id": 1,
            "title": "Мастер и Маргарита",
            "author": "Булгаков",
            "year": 1967,
            "available": True
        },
        {
            "id": 2,
            "title": "Преступление и наказание",
            "author": "Достоевский",
            "year": 1866,
            "available": False
        }
    ]

    try:
        with open(FILE_NAME, 'w', encoding='utf-8') as file:
            json.dump(default_books, file, ensure_ascii=False, indent=4)
        print("Файл library.json создан с тестовыми данными")
    except Exception as error:
        print(f"Ошибка при создании файла: {error}")


def show_all_books(books):
    if not books:
        print("Библиотека пуста")
        return

    print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Доступна':<10}")
    for book in books:
        status = "Да" if book['available'] else "Нет"
        print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} "
              f"{book['year']:<6} {status:<10}")


def search_books(books):
    query = input("Введите название или автора для поиска: ").strip().lower()
    if not query:
        print("Ошибка: поисковый запрос не может быть пустым")
        return

    found = []
    for book in books:
        if query in book['title'].lower() or query in book['author'].lower():
            found.append(book)

    if found:
        print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Доступна':<10}")
        for book in found:
            status = "Да" if book['available'] else "Нет"
            print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} "
                  f"{book['year']:<6} {status:<10}")
    else:
        print("Книги не найдены")


def add_book(books):
    try:
        new_id = max(book['id'] for book in books) + 1 if books else 1
    except ValueError:
        new_id = 1

    title = input("Введите название книги: ").strip()
    if not title:
        print("Ошибка: название не может быть пустым")
        return books

    author = input("Введите автора книги: ").strip()
    if not author:
        print("Ошибка: автор не может быть пустым")
        return books

    try:
        year = int(input("Введите год издания: "))
        if year <= 0 or year > 2026:
            print("Ошибка: некорректный год")
            return books
    except ValueError:
        print("Ошибка: год должен быть целым числом")
        return books

    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "year": year,
        "available": True
    }

    books.append(new_book)
    save_books(books)
    print(f"Книга '{title}' успешно добавлена с ID {new_id}")
    return books


def change_status(books):
    try:
        book_id = int(input("Введите ID книги: "))
    except ValueError:
        print("Ошибка: ID должен быть числом")
        return books

    for book in books:
        if book['id'] == book_id:
            current_status = "доступна" if book['available'] else "не доступна"
            print(f"Текущий статус: {current_status}")

            new_status = input("Введите новый статус (доступна/недоступна): ").strip().lower()

            if new_status in ['доступна', 'да', 'true', 'yes']:
                book['available'] = True
                print("Статус изменен на 'доступна'")
            elif new_status in ['недоступна', 'нет', 'false', 'no']:
                book['available'] = False
                print("Статус изменен на 'недоступна'")
            else:
                print("Ошибка: неверный статус")

            save_books(books)
            return books

    print(f"Книга с ID {book_id} не найдена")
    return books


def delete_book(books):
    try:
        book_id = int(input("Введите ID книги для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом")
        return books

    for i, book in enumerate(books):
        if book['id'] == book_id:
            confirm = input(f"Удалить книгу '{book['title']}'? (да/нет): ").strip().lower()
            if confirm in ['да', 'yes', 'д']:
                books.pop(i)
                save_books(books)
                print(f"Книга с ID {book_id} удалена")
            else:
                print("Удаление отменено")
            return books

    print(f"Книга с ID {book_id} не найдена")
    return books


def export_available_books(books):
    available = [book for book in books if book['available']]

    if not available:
        print("Нет доступных книг для экспорта")
        return

    try:
        with open('resource/available_books.txt', 'w', encoding='utf-8') as file:
            file.write("Список доступных книг:\n")
            for book in available:
                file.write(f"ID: {book['id']}\n")
                file.write(f"Название: {book['title']}\n")
                file.write(f"Автор: {book['author']}\n")
                file.write(f"Год: {book['year']}\n")

        print(f"Экспортировано {len(available)} книг в файл available_books.txt")
    except Exception:
        print("Ошибка: не удалось экспортировать книги")


def main():
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            pass
    except FileNotFoundError:
        create_library_file()

    books = load_books()

    while True:
        print("СИСТЕМА УЧЕТА КНИГ В БИБЛИОТЕКЕ")
        print("1. Просмотр всех книг")
        print("2. Поиск по автору/названию")
        print("3. Добавление новой книги")
        print("4. Изменение статуса доступности")
        print("5. Удаление книги по ID")
        print("6. Экспорт доступных книг в файл")
        print("7. Сохранить и выйти")
        print("=" * 50)

        choice = input("Выберите действие (1-7): ").strip()

        match choice:
            case '1':
                show_all_books(books)
            case '2':
                search_books(books)
            case '3':
                books = add_book(books)
            case '4':
                books = change_status(books)
            case '5':
                books = delete_book(books)
            case '6':
                export_available_books(books)
            case '7':
                save_books(books)
                print("Данные сохранены. До свидания!")
                break
            case _:
                print("Ошибка: выберите действие от 1 до 7")


if __name__ == "__main__":
    main()