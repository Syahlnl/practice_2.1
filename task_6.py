def read_uint16_little(data, offset):
    return data[offset] + (data[offset + 1] << 8)


def read_uint32_little(data, offset):
    return (data[offset] + (data[offset + 1] << 8) +
            (data[offset + 2] << 16) + (data[offset + 3] << 24))


def read_uint64_little(data, offset):
    return (data[offset] + (data[offset + 1] << 8) +
            (data[offset + 2] << 16) + (data[offset + 3] << 24) +
            (data[offset + 4] << 32) + (data[offset + 5] << 40) +
            (data[offset + 6] << 48) + (data[offset + 7] << 56))


def read_int16_little(data, offset):
    value = read_uint16_little(data, offset)
    if value >= 32768:
        return value - 65536
    return value


def parse_binary_file(filename):
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()

        if len(file_data) < 10:
            print("Ошибка: файл слишком маленький")
            return None

        if file_data[0:4] != b'DATA':
            print("Ошибка: неверная сигнатура файла")
            return None

        version = read_uint16_little(file_data, 4)
        records_count = read_uint32_little(file_data, 6)

        print(f"Версия файла: {version}")
        print(f"Количество записей: {records_count}")

        records = []
        active_flags_count = 0
        total_temperature = 0
        position = 10

        for i in range(records_count):
            if position + 15 > len(file_data):
                print(f"Ошибка: запись {i + 1} повреждена")
                break

            timestamp = read_uint64_little(file_data, position)
            record_id = read_uint32_little(file_data, position + 8)
            temperature_raw = read_int16_little(file_data, position + 12)
            temperature = temperature_raw / 100.0
            flags = file_data[position + 14]

            records.append({
                'timestamp': timestamp,
                'id': record_id,
                'temperature': temperature,
                'flags': flags
            })

            total_temperature += temperature

            if flags & 0x01:
                active_flags_count += 1

            position += 15

        return {
            'records': records,
            'total_temperature': total_temperature,
            'active_flags_count': active_flags_count,
            'records_count': records_count
        }

    except FileNotFoundError:
        print("Ошибка: файл не найден")
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None


def show_statistics(data):
    if not data or data['records_count'] == 0:
        print("Нет данных для анализа")
        return

    avg_temperature = data['total_temperature'] / data['records_count']

    print("СТАТИСТИКА")
    print(f"Средняя температура: {avg_temperature:.2f}°C")
    print(f"Количество активных флагов: {data['active_flags_count']}")
    print(f"Всего записей: {data['records_count']}")


def show_all_records(data):
    if not data or not data['records']:
        print("Нет записей для отображения")
        return

    print(f"{'№':<5} {'Timestamp':<20} {'ID':<10} {'Температура':<15} {'Флаги':<10}")

    for i, record in enumerate(data['records']):
        flags_binary = format(record['flags'], '08b')
        print(f"{i + 1:<5} {record['timestamp']:<20} {record['id']:<10} "
              f"{record['temperature']:.2f}°C{'':<10} {flags_binary}")


def create_sample_binary_file(filename="resource/data.bin"):
    try:
        with open(filename, 'wb') as file:
            file.write(b'DATA')

            file.write(bytes([1, 0]))

            file.write(bytes([3, 0, 0, 0]))

            timestamp1 = 1700000000
            file.write(bytes([
                timestamp1 & 0xFF,
                (timestamp1 >> 8) & 0xFF,
                (timestamp1 >> 16) & 0xFF,
                (timestamp1 >> 24) & 0xFF,
                (timestamp1 >> 32) & 0xFF,
                (timestamp1 >> 40) & 0xFF,
                (timestamp1 >> 48) & 0xFF,
                (timestamp1 >> 56) & 0xFF
            ]))

            file.write(bytes([0xE9, 0x03, 0x00, 0x00]))

            file.write(bytes([0x2E, 0x09]))

            file.write(bytes([0x01]))

            timestamp2 = 1700000100
            file.write(bytes([
                timestamp2 & 0xFF,
                (timestamp2 >> 8) & 0xFF,
                (timestamp2 >> 16) & 0xFF,
                (timestamp2 >> 24) & 0xFF,
                (timestamp2 >> 32) & 0xFF,
                (timestamp2 >> 40) & 0xFF,
                (timestamp2 >> 48) & 0xFF,
                (timestamp2 >> 56) & 0xFF
            ]))

            file.write(bytes([0xEA, 0x03, 0x00, 0x00]))

            file.write(bytes([0x6A, 0xFE]))

            file.write(bytes([0x00]))

            timestamp3 = 1700000200
            file.write(bytes([
                timestamp3 & 0xFF,
                (timestamp3 >> 8) & 0xFF,
                (timestamp3 >> 16) & 0xFF,
                (timestamp3 >> 24) & 0xFF,
                (timestamp3 >> 32) & 0xFF,
                (timestamp3 >> 40) & 0xFF,
                (timestamp3 >> 48) & 0xFF,
                (timestamp3 >> 56) & 0xFF
            ]))

            file.write(bytes([0xEB, 0x03, 0x00, 0x00]))

            file.write(bytes([0x42, 0x0E]))

            file.write(bytes([0x01]))

        print(f"Создан пример файла {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return False


def main():
    print("ПАРСЕР БИНАРНЫХ ФАЙЛОВ")

    filename = "resource/data.bin"

    try:
        with open(filename, 'rb') as file:
            pass
    except FileNotFoundError:
        print(f"Файл {filename} не найден, создаю автоматически...")
        if not create_sample_binary_file(filename):
            return

    data = parse_binary_file(filename)

    if data:
        show_all_records(data)
        show_statistics(data)


if __name__ == "__main__":
    main()