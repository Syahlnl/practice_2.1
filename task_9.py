import re


def serialize_to_json(obj, indent=None, level=0):
    if indent is None:
        spaces = ""
    else:
        spaces = " " * (indent * level)
        next_spaces = " " * (indent * (level + 1))

    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for key, value in obj.items():
            serialized_key = f'"{key}"'
            serialized_value = serialize_to_json(value, indent, level + 1 if indent else 0)
            if indent is None:
                items.append(f"{serialized_key}:{serialized_value}")
            else:
                items.append(f"{next_spaces}{serialized_key}: {serialized_value}")
        if indent is None:
            return "{" + ",".join(items) + "}"
        else:
            return "{\n" + ",\n".join(items) + f"\n{spaces}" + "}"

    elif isinstance(obj, list):
        if not obj:
            return "[]"
        items = []
        for value in obj:
            serialized_value = serialize_to_json(value, indent, level + 1 if indent else 0)
            if indent is None:
                items.append(serialized_value)
            else:
                items.append(f"{next_spaces}{serialized_value}")
        if indent is None:
            return "[" + ",".join(items) + "]"
        else:
            return "[\n" + ",\n".join(items) + f"\n{spaces}" + "]"

    elif isinstance(obj, str):
        escaped = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        return f'"{escaped}"'

    elif isinstance(obj, bool):
        return "true" if obj else "false"

    elif isinstance(obj, (int, float)):
        return str(obj)

    elif obj is None:
        return "null"

    else:
        raise TypeError(f"Неподдерживаемый тип: {type(obj)}")


def parse_json(json_str):
    def skip_whitespace(pos):
        while pos < len(json_str) and json_str[pos] in ' \t\n\r':
            pos += 1
        return pos

    def parse_value(pos):
        pos = skip_whitespace(pos)

        if pos >= len(json_str):
            raise ValueError("Неожиданный конец строки")

        if json_str[pos] == '{':
            return parse_object(pos)
        elif json_str[pos] == '[':
            return parse_array(pos)
        elif json_str[pos] == '"':
            return parse_string(pos)
        elif json_str[pos] == 't' and json_str.startswith('true', pos):
            return True, pos + 4
        elif json_str[pos] == 'f' and json_str.startswith('false', pos):
            return False, pos + 5
        elif json_str[pos] == 'n' and json_str.startswith('null', pos):
            return None, pos + 4
        elif json_str[pos] in '-0123456789':
            return parse_number(pos)
        else:
            raise ValueError(f"Неожиданный символ на позиции {pos}: {json_str[pos]}")

    def parse_object(pos):
        pos = skip_whitespace(pos + 1)
        obj = {}

        if json_str[pos] == '}':
            return obj, pos + 1

        while True:
            pos = skip_whitespace(pos)
            if json_str[pos] != '"':
                raise ValueError(f"Ожидалась строка в качестве ключа на позиции {pos}")

            key, pos = parse_string(pos)
            pos = skip_whitespace(pos)

            if pos >= len(json_str) or json_str[pos] != ':':
                raise ValueError(f"Ожидалось ':' после ключа на позиции {pos}")

            pos = skip_whitespace(pos + 1)
            value, pos = parse_value(pos)
            obj[key] = value

            pos = skip_whitespace(pos)
            if pos >= len(json_str):
                raise ValueError("Неожиданный конец строки")

            if json_str[pos] == '}':
                return obj, pos + 1
            elif json_str[pos] == ',':
                pos = skip_whitespace(pos + 1)
            else:
                raise ValueError(f"Ожидалась ',' или '}}' на позиции {pos}")

    def parse_array(pos):
        pos = skip_whitespace(pos + 1)
        arr = []

        if json_str[pos] == ']':
            return arr, pos + 1

        while True:
            value, pos = parse_value(pos)
            arr.append(value)

            pos = skip_whitespace(pos)
            if pos >= len(json_str):
                raise ValueError("Неожиданный конец строки")

            if json_str[pos] == ']':
                return arr, pos + 1
            elif json_str[pos] == ',':
                pos = skip_whitespace(pos + 1)
            else:
                raise ValueError(f"Ожидалась ',' или ']' на позиции {pos}")

    def parse_string(pos):
        pos += 1
        start = pos
        while pos < len(json_str) and json_str[pos] != '"':
            if json_str[pos] == '\\':
                pos += 2
            else:
                pos += 1

        if pos >= len(json_str):
            raise ValueError("Незакрытая строка")

        value = json_str[start:pos]
        value = value.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '\n')
        return value, pos + 1

    def parse_number(pos):
        start = pos
        while pos < len(json_str) and json_str[pos] in '-0123456789.eE':
            pos += 1

        num_str = json_str[start:pos]
        try:
            if '.' in num_str or 'e' in num_str or 'E' in num_str:
                return float(num_str), pos
            else:
                return int(num_str), pos
        except ValueError:
            raise ValueError(f"Неверное число на позиции {start}: {num_str}")

    try:
        result, pos = parse_value(0)
        pos = skip_whitespace(pos)
        if pos < len(json_str):
            raise ValueError(f"Лишние символы после JSON на позиции {pos}")
        return result
    except ValueError as e:
        line_num = json_str[:e.args[0].split()[-1] if 'позиции' in str(e) else 0].count('\n') + 1
        raise ValueError(f"Ошибка на строке {line_num}: {e}")


def validate_json(json_str):
    try:
        parse_json(json_str)
        print("JSON валиден")
        return True
    except ValueError as e:
        print(f"Ошибка валидации: {e}")
        return False


def print_json_with_indent(json_obj, indent=4):
    json_str = serialize_to_json(json_obj, indent)
    print(json_str)


def main():
    print("=" * 50)
    print("СЕРИАЛИЗАЦИЯ И ДЕСЕРИАЛИЗАЦИЯ JSON")
    print("=" * 50)

    test_objects = [
        '{"name": "John", "age": 30, "city": "New York"}',
        '{"numbers": [1, 2, 3, 4, 5], "active": true, "value": null}',
        '{"person": {"name": "Alice", "address": {"city": "London", "zip": 12345}}}',
        '{"invalid": "test",}',
        '{"missing_quote": "value}'
    ]

    print("\n1. Тестирование валидации JSON:")
    print("-" * 50)
    for i, test_str in enumerate(test_objects, 1):
        print(f"\nТест {i}:")
        print(f"Строка: {test_str}")
        validate_json(test_str)

    print("\n" + "=" * 50)
    print("2. Сериализация Python объекта в JSON:")
    print("-" * 50)

    python_obj = {
        "name": "Test User",
        "age": 25,
        "is_student": True,
        "grades": [85, 90, 78, 92],
        "address": {
            "city": "Moscow",
            "street": "Tverskaya"
        },
        "score": None
    }

    print("Исходный Python объект:")
    print(python_obj)

    print("\nСериализованный JSON (без отступов):")
    json_str = serialize_to_json(python_obj)
    print(json_str)

    print("\nСериализованный JSON (с отступами 4):")
    print_json_with_indent(python_obj, 4)

    print("\n" + "=" * 50)
    print("3. Десериализация JSON в Python объект:")
    print("-" * 50)

    json_test = '{"products": [{"name": "Apple", "price": 100}, {"name": "Banana", "price": 80}], "total": 180}'
    print(f"JSON строка: {json_test}")

    parsed = parse_json(json_test)
    print(f"Десериализованный объект: {parsed}")

    print("\n4. Проверка на вложенных структурах:")
    print("-" * 50)

    nested_json = '{"level1": {"level2": {"level3": [1, 2, {"deep": "value"}]}}}'
    print(f"Вложенный JSON: {nested_json}")
    parsed_nested = parse_json(nested_json)
    print(f"Успешно десериализован: {parsed_nested}")

    print("\n" + "=" * 50)
    print("ГОТОВО")
    print("=" * 50)


if __name__ == "__main__":
    main()