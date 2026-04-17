import re


def validate_xml(xml_str):
    lines = xml_str.splitlines()
    stack = []
    tag_re = re.compile(r'<(\/?)([\w\-\.]+)([^>]*)>')

    for i, line in enumerate(lines, 1):
        for match in tag_re.finditer(line):
            closing = match.group(1)
            tag_name = match.group(2)
            attrs = match.group(3).strip()

            if attrs and not re.match(r'^([\w\-\.]+\s*=\s*"[^"]*"\s*)*$', attrs):
                print(f"Ошибка в строке {i}: неверные атрибуты у тега <{tag_name}>")
                return False

            if closing == '/':
                if not stack or stack[-1] != tag_name:
                    print(f"Ошибка в строке {i}: лишний закрывающий тег </{tag_name}>")
                    return False
                stack.pop()
            elif match.group(0).endswith('/>'):
                continue
            else:
                stack.append(tag_name)

    if stack:
        print(f"Ошибка: не закрыты теги {', '.join(stack)}")
        return False

    print("XML валиден")
    return True


def serialize_to_xml(obj, root_tag="root", indent=2):
    def _serialize(data, level=0):
        spaces = " " * (level * indent)
        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                if isinstance(value, list):
                    for item in value:
                        result.append(f"{spaces}<{key}>")
                        result.append(_serialize(item, level + 1))
                        result.append(f"{spaces}</{key}>")
                elif isinstance(value, dict):
                    result.append(f"{spaces}<{key}>")
                    result.append(_serialize(value, level + 1))
                    result.append(f"{spaces}</{key}>")
                elif value is None:
                    result.append(f"{spaces}<{key}/>")
                else:
                    value_str = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    result.append(f"{spaces}<{key}>{value_str}</{key}>")
            return "\n".join(result)
        elif isinstance(data, list):
            return "\n".join(_serialize(item, level) for item in data)
        else:
            return f"{spaces}{str(data)}"

    xml_lines = [f"<{root_tag}>", _serialize(obj, 1), f"</{root_tag}>"]
    return "\n".join(xml_lines)


def deserialize_from_xml(xml_str):
    xml_str = re.sub(r'>\s+<', '><', xml_str.strip())

    def _parse_element(tag_content):
        result = {}
        pattern = r'<(\/?)([\w\-\.]+)([^>]*)>'
        pos = 0
        while pos < len(tag_content):
            match = re.search(pattern, tag_content[pos:])
            if not match:
                break

            tag_name = match.group(2)
            start = pos + match.start()
            end = pos + match.end()

            if tag_name.startswith('/'):
                break

            next_match = re.search(pattern, tag_content[end:])
            if next_match and next_match.group(1) == '/' and next_match.group(2) == tag_name:
                inner_content = tag_content[end:end + next_match.start()]
                value = _parse_element(inner_content) if '<' in inner_content else inner_content.strip()
                if tag_name in result:
                    if not isinstance(result[tag_name], list):
                        result[tag_name] = [result[tag_name]]
                    result[tag_name].append(value)
                else:
                    result[tag_name] = value
                pos = end + next_match.end()
            else:
                pos = end

        return result if result else tag_content.strip()

    root_match = re.search(r'<([\w\-\.]+)>(.*)</\1>', xml_str, re.DOTALL)
    if root_match:
        return _parse_element(root_match.group(2))
    return {}


def test_with_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        print(f"\n=== {filepath} ===")
        print("Валидация:")
        if validate_xml(xml_content):
            print("Десериализация:")
            obj = deserialize_from_xml(xml_content)
            print(obj)
            print("\nСериализация обратно:")
            print(serialize_to_xml(obj, "root"))
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    test_files = [
        "resource/test_1.xml",
        "resource/test_2.xml",
        "resource/test_3.xml",
        "resource/test_4.xml",
        "resource/test_5.xml",
        "resource/test_6.xml",
        "resource/test_7.xml"
    ]

    for file in test_files:
        test_with_file(file)