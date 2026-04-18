import csv

FILE_NAME = 'resource/products.csv'
SORTED_FILE_NAME = 'resource/sorted_products.csv'


def create_initial_file():
    try:
        with open(FILE_NAME, 'r', encoding='utf-8', newline='') as file:
            pass
    except FileNotFoundError:
        content = [
            ['Название', 'Цена', 'Количество'],
            ['Яблоки', '100', '50'],
            ['Бананы', '80', '30'],
            ['Молоко', '120', '20'],
            ['Хлеб', '40', '100']
        ]
        try:
            with open(FILE_NAME, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(content)
            print("Файл products.csv успешно создан с начальными данными\n")
        except Exception as error:
            print(f"Ошибка при создании файла: {error}")


def read_products():
    products = []
    try:
        with open(FILE_NAME, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 3 and row[0] and row[1] and row[2]:
                    products.append({
                        'Название': row[0],
                        'Цена': row[1],
                        'Количество': row[2]
                    })
        print(f"Загружено {len(products)} товаров из файла")
        return products
    except FileNotFoundError:
        print("Ошибка: Файл не найден. Создайте его сначала.")
        return []
    except Exception as error:
        print(f"Ошибка при чтении файла: {error}")
        return []


def display_products(products):
    if not products:
        print("Список товаров пуст")
        return

    print("\nТекущий список товаров:")
    print(f"{'Название':<15} {'Цена':<10} {'Количество':<10}")
    for product in products:
        print(f"{product['Название']:<15} {product['Цена']:<10} {product['Количество']:<10}")


def add_product(products):
    try:
        name = input("Введите название товара: ").strip()
        if not name:
            print("Ошибка: Название не может быть пустым")
            return products

        price = input("Введите цену товара: ").strip()
        if not price.isdigit():
            print("Ошибка: Цена должна быть числом")
            return products

        quantity = input("Введите количество товара: ").strip()
        if not quantity.isdigit():
            print("Ошибка: Количество должно быть числом")
            return products

        products.append({'Название': name, 'Цена': price, 'Количество': quantity})
        print(f"Товар '{name}' успешно добавлен")

        save_products(products)

    except Exception as error:
        print(f"Ошибка при добавлении товара: {error}")

    return products


def search_product(products):
    if not products:
        print("Список товаров пуст")
        return

    search_name = input("Введите название товара для поиска: ").strip().lower()
    found = False

    print("\nРезультаты поиска:")
    for product in products:
        if product['Название'].lower() == search_name:
            print(f"Найден товар: {product['Название']}, Цена: {product['Цена']}, "
                  f"Количество: {product['Количество']}")
            found = True
            break

    if not found:
        print(f"Товар '{search_name}' не найден")


def calculate_total_value(products):
    if not products:
        print("Список товаров пуст")
        return

    total = 0
    for product in products:
        try:
            price = int(product['Цена'])
            quantity = int(product['Количество'])
            total += price * quantity
        except ValueError:
            print(f"Ошибка в данных товара: {product['Название']}")
            continue

    print(f"\nОбщая стоимость всех товаров на складе: {total} руб.")


def save_products(products):
    try:
        with open(FILE_NAME, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Название', 'Цена', 'Количество'])
            for product in products:
                writer.writerow([product['Название'], product['Цена'], product['Количество']])
        print("Данные успешно сохранены в файл")
    except Exception as error:
        print(f"Ошибка при сохранении файла: {error}")


def save_sorted_products(products):
    if not products:
        print("Список товаров пуст")
        return

    try:
        sorted_products = sorted(products, key=lambda x: int(x['Цена']))

        with open(SORTED_FILE_NAME, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Название', 'Цена', 'Количество'])
            for product in sorted_products:
                writer.writerow([product['Название'], product['Цена'], product['Количество']])

        print(f"Отсортированные по цене товары сохранены в файл {SORTED_FILE_NAME}")

        print("\nОтсортированный список товаров по цене:")
        print(f"{'Название':<15} {'Цена':<10} {'Количество':<10}")
        for product in sorted_products:
            print(f"{product['Название']:<15} {product['Цена']:<10} {product['Количество']:<10}")

    except Exception as error:
        print(f"Ошибка при сохранении отсортированного файла: {error}")


def main():
    create_initial_file()
    products = read_products()

    while True:
        print("МЕНЮ:")
        print("1. Показать все товары")
        print("2. Добавить новый товар")
        print("3. Поиск товара по названию")
        print("4. Расчет общей стоимости всех товаров")
        print("5. Сохранить данные в файл")
        print("6. Сохранить отсортированные по цене товары")
        print("7. Выход")

        choice = input("Выберите пункт меню (1-7): ").strip()

        match choice:
            case "1":
                display_products(products)
            case "2":
                products = add_product(products)
            case "3":
                search_product(products)
            case "4":
                calculate_total_value(products)
            case "5":
                save_products(products)
            case "6":
                save_sorted_products(products)
            case "7":
                save_choice = input("Сохранить изменения перед выходом? (да/нет): ").strip().lower()
                if save_choice == "да":
                    save_products(products)
                print("До свидания!")
                break
            case _:
                print("Ошибка: Неверный выбор. Пожалуйста, выберите пункт от 1 до 7")


if __name__ == '__main__':
    main()