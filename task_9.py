import re
import os


def validate_json(json_str):
    lines = json_str.splitlines()
    stack = []
    in_string = False
    escape = False

    for i, line in enumerate(lines, 1):
        for j, char in enumerate(line):
            if escape:
                escape = False
                continue

            if char == '\\' and in_string:
                escape = True
                continue

            if char == '"' and not escape:
                in_string = not in_string
                continue

            if not in_string:
                if char in '{[':
                    stack.append((char, i, j))
                elif char == '}':
                    if not stack or stack[-1][0] != '{':
                        print(f"Ошибка в строке {i}: лишняя скобка }}")
                        return False
                    stack.pop()
                elif char == ']':
                    if not stack or stack[-1][0] != '[':
                        print(f"Ошибка в строке {i}: лишняя скобка ]")
                        return False
                    stack.pop()

    if in_string:
        print("Ошибка: незакрытая строка")
        return False

    if stack:
        print(f"Ошибка: не закрыты {len(stack)} скобок")
        return False

    try:
        _parse_value(json_str.strip())
        print("JSON валиден")
        return True
    except Exception as e:
        print(f"Ошибка валидации: {e}")
        return False


def _parse_value(value_str):
    value_str = value_str.strip()

    if not value_str:
        raise ValueError("Пустое значение")

    if value_str == 'null':
        return None
    elif value_str == 'true':
        return True
    elif value_str == 'false':
        return False
    elif value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]
    elif value_str.startswith('{'):
        return _parse_object(value_str)
    elif value_str.startswith('['):
        return _parse_array(value_str)
    elif value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
        return int(value_str)
    elif re.match(r'^-?\d+\.\d+$', value_str):
        return float(value_str)
    else:
        raise ValueError(f"Неизвестный тип: {value_str}")


def _parse_object(obj_str):
    obj_str = obj_str.strip()
    if not obj_str.startswith('{') or not obj_str.endswith('}'):
        raise ValueError("Неверный формат объекта")

    if obj_str == '{}':
        return {}

    content = obj_str[1:-1].strip()
    result = {}
    parts = []
    current = ""
    in_string = False
    escape = False
    bracket_count = 0
    array_count = 0

    for char in content:
        if escape:
            current += char
            escape = False
            continue

        if char == '\\' and in_string:
            current += char
            escape = True
            continue

        if char == '"' and not escape:
            in_string = not in_string
            current += char
            continue

        if not in_string:
            if char == '{':
                bracket_count += 1
            elif char == '}':
                bracket_count -= 1
            elif char == '[':
                array_count += 1
            elif char == ']':
                array_count -= 1

            if char == ',' and bracket_count == 0 and array_count == 0:
                parts.append(current.strip())
                current = ""
                continue

        current += char

    if current.strip():
        parts.append(current.strip())

    for part in parts:
        if ':' not in part:
            raise ValueError(f"Неверный формат: {part}")

        colon_pos = part.find(':')
        key_part = part[:colon_pos].strip()
        value_part = part[colon_pos + 1:].strip()

        if not (key_part.startswith('"') and key_part.endswith('"')):
            raise ValueError(f"Ключ должен быть в кавычках: {key_part}")

        key = key_part[1:-1]
        result[key] = _parse_value(value_part)

    return result


def _parse_array(array_str):
    array_str = array_str.strip()
    if not array_str.startswith('[') or not array_str.endswith(']'):
        raise ValueError("Неверный формат массива")

    if array_str == '[]':
        return []

    content = array_str[1:-1].strip()
    items = []
    current = ""
    in_string = False
    escape = False
    bracket_count = 0
    array_count = 0

    for char in content:
        if escape:
            current += char
            escape = False
            continue

        if char == '\\' and in_string:
            current += char
            escape = True
            continue

        if char == '"' and not escape:
            in_string = not in_string
            current += char
            continue

        if not in_string:
            if char == '{':
                bracket_count += 1
            elif char == '}':
                bracket_count -= 1
            elif char == '[':
                array_count += 1
            elif char == ']':
                array_count -= 1

            if char == ',' and bracket_count == 0 and array_count == 0:
                items.append(_parse_value(current.strip()))
                current = ""
                continue

        current += char

    if current.strip():
        items.append(_parse_value(current.strip()))

    return items


def deserialize_from_json(json_str):
    return _parse_value(json_str.strip())


def serialize_to_json(obj, indent=2):
    def _serialize(data, level=0, indent_size=2):
        spaces = " " * (level * indent_size) if indent_size else ""
        next_spaces = " " * ((level + 1) * indent_size) if indent_size else ""

        if data is None:
            return "null"
        elif isinstance(data, bool):
            return "true" if data else "false"
        elif isinstance(data, (int, float)):
            return str(data)
        elif isinstance(data, str):
            return f'"{data}"'
        elif isinstance(data, (list, tuple)):
            if not data:
                return "[]"
            if indent_size:
                items = [f"{next_spaces}{_serialize(item, level + 1, indent_size)}" for item in data]
                return f"[\n{',\n'.join(items)}\n{spaces}]"
            else:
                items = [_serialize(item, level, None) for item in data]
                return f"[{', '.join(items)}]"
        elif isinstance(data, dict):
            if not data:
                return "{}"
            if indent_size:
                items = []
                for key, value in data.items():
                    serialized_value = _serialize(value, level + 1, indent_size)
                    items.append(f'{next_spaces}"{key}": {serialized_value}')
                return f"{{\n{',\n'.join(items)}\n{spaces}}}"
            else:
                items = [f'"{key}": {_serialize(value, level, None)}' for key, value in data.items()]
                return f"{{{', '.join(items)}}}"
        else:
            raise TypeError(f"Тип {type(data)} не сериализуем")

    return _serialize(obj, 0, indent)


def test_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"\n=== {filepath} ===")
        print("Валидация:")
        if validate_json(content):
            print("Десериализация:")
            obj = deserialize_from_json(content)
            print(obj)
            print("\nСериализация обратно:")
            print(serialize_to_json(obj, 2))
    except FileNotFoundError:
        print(f"Ошибка: файл {filepath} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")


def main():
    for i in range(1, 11):
        filename = f"test_{i}.json"
        filepath = os.path.join("resource", filename)
        test_file(filepath)


if __name__ == "__main__":
    main()