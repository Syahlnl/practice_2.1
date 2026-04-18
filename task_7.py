def cyclic_left_shift(byte, shift):
    shift = shift % 8
    return ((byte << shift) | (byte >> (8 - shift))) & 0xFF


def cyclic_right_shift(byte, shift):
    shift = shift % 8
    return ((byte >> shift) | (byte << (8 - shift))) & 0xFF


def encrypt_byte(byte, key):
    shifted = cyclic_left_shift(byte, 2)
    encrypted = shifted ^ key
    return encrypted


def decrypt_byte(byte, key):
    xored = byte ^ key
    decrypted = cyclic_right_shift(xored, 2)
    return decrypted


def process_file(input_filename, output_filename, key, mode='encrypt'):
    try:
        with open(input_filename, 'rb') as input_file:
            data = input_file.read()

        if not data:
            print("Ошибка: файл пуст")
            return False

        processed_data = bytearray()

        for byte in data:
            if mode == 'encrypt':
                processed_byte = encrypt_byte(byte, key)
            else:
                processed_byte = decrypt_byte(byte, key)
            processed_data.append(processed_byte)

        with open(output_filename, 'wb') as output_file:
            output_file.write(processed_data)

        mode_text = "Зашифрован" if mode == 'encrypt' else "Расшифрован"
        print(f"{mode_text} файл сохранен как {output_filename}")
        return True

    except FileNotFoundError:
        print("Ошибка: входной файл не найден")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def get_key():
    try:
        key_input = input("Введите ключ (0-255): ").strip()
        key = int(key_input)
        if 0 <= key <= 255:
            return key
        else:
            print("Ошибка: ключ должен быть в диапазоне 0-255")
            return None
    except ValueError:
        print("Ошибка: ключ должен быть целым числом")
        return None


def main():
    print("ШИФРОВАНИЕ БИНАРНЫХ ФАЙЛОВ")

    while True:
        print("\n1. Зашифровать файл")
        print("2. Расшифровать файл")
        print("3. Выйти")

        choice = input("Выберите действие (1-3): ").strip()

        match choice:
            case '1':
                input_file = input("Введите имя входного файла: ").strip()
                if not input_file:
                    print("Ошибка: имя файла не может быть пустым")
                    continue

                output_file = input("Введите имя выходного файла: ").strip()
                if not output_file:
                    output_file = "encrypted_" + input_file

                key = get_key()
                if key is None:
                    continue

                process_file(input_file, output_file, key, 'encrypt')

            case '2':
                input_file = input("Введите имя зашифрованного файла: ").strip()
                if not input_file:
                    print("Ошибка: имя файла не может быть пустым")
                    continue

                output_file = input("Введите имя выходного файла: ").strip()
                if not output_file:
                    output_file = "decrypted_" + input_file

                key = get_key()
                if key is None:
                    continue

                process_file(input_file, output_file, key, 'decrypt')

            case '3':
                print("До свидания!")
                break

            case _:
                print("Ошибка: выберите действие от 1 до 3")


if __name__ == "__main__":
    main()