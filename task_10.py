import re
from typing import Any, Dict, List, Union


class XMLSerializer:
    """Класс для сериализации и десериализации XML без использования сторонних библиотек."""

    @staticmethod
    def _escape_xml(text: str) -> str:
        """Замена специальных символов на XML-сущности."""
        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&apos;"
        }
        for char, entity in replacements.items():
            text = text.replace(char, entity)
        return text

    @staticmethod
    def _unescape_xml(text: str) -> str:
        """Восстановление символов из XML-сущностей."""
        replacements = {
            "&amp;": "&",
            "&lt;": "<",
            "&gt;": ">",
            "&quot;": '"',
            "&apos;": "'"
        }
        for entity, char in replacements.items():
            text = text.replace(entity, char)
        return text

    @staticmethod
    def serialize(obj: Any, root_tag: str = "root", indent: int = 2) -> str:
        """
        Сериализует Python-объект в XML-строку.

        Args:
            obj: Объект для сериализации (dict, list, str, int, float, bool, None)
            root_tag: Имя корневого тега
            indent: Количество пробелов для отступа (0 - без форматирования)

        Returns:
            XML-строка
        """
        def _serialize(data: Any, tag: str, level: int) -> str:
            spaces = " " * (indent * level) if indent > 0 else ""
            next_spaces = " " * (indent * (level + 1)) if indent > 0 else ""

            # Обработка примитивных типов
            if isinstance(data, (str, int, float, bool, type(None))):
                if data is None:
                    value = "null"
                elif isinstance(data, bool):
                    value = "true" if data else "false"
                else:
                    value = str(data)
                if indent > 0:
                    return f"{spaces}<{tag}>{XMLSerializer._escape_xml(value)}</{tag}>\n"
                return f"<{tag}>{XMLSerializer._escape_xml(value)}</{tag}>"

            # Обработка списка
            if isinstance(data, list):
                result = ""
                for item in data:
                    result += _serialize(item, tag, level)
                return result

            # Обработка словаря
            if isinstance(data, dict):
                attributes = data.get("@attributes", {})
                attr_str = ""
                for attr_name, attr_val in attributes.items():
                    attr_str += f' {attr_name}="{XMLSerializer._escape_xml(str(attr_val))}"'

                text_content = data.get("#text", "")
                children = {k: v for k, v in data.items() if not k.startswith("@") and k != "#text"}

                if indent > 0:
                    opening_tag = f"{spaces}<{tag}{attr_str}>"
                else:
                    opening_tag = f"<{tag}{attr_str}>"

                # Если есть дочерние элементы
                if children:
                    result = opening_tag + "\n"
                    for child_tag, child_data in children.items():
                        result += _serialize(child_data, child_tag, level + 1)
                    if indent > 0:
                        result += f"{spaces}</{tag}>\n"
                    else:
                        result += f"</{tag}>"
                    return result
                # Если есть только текстовое содержимое
                elif text_content or text_content == "":
                    if indent > 0:
                        return f"{opening_tag}{XMLSerializer._escape_xml(str(text_content))}</{tag}>\n"
                    return f"{opening_tag}{XMLSerializer._escape_xml(str(text_content))}</{tag}>"
                # Пустой элемент
                else:
                    if indent > 0:
                        return f"{spaces}<{tag}{attr_str} />\n"
                    return f"<{tag}{attr_str} />"

            raise TypeError(f"Неподдерживаемый тип для сериализации: {type(data)}")

        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        return xml_declaration + _serialize(obj, root_tag, 0).rstrip()

    @staticmethod
    def deserialize(xml_str: str) -> Dict[str, Any]:
        """
        Десериализует XML-строку в Python-объект.

        Args:
            xml_str: XML-строка для парсинга

        Returns:
            Python-объект (dict)

        Raises:
            ValueError: При синтаксических ошибках в XML
        """
        xml_str = xml_str.strip()
        lines = xml_str.split('\n')

        class XMLParser:
            def __init__(self, content: str, lines: List[str]):
                self.content = content
                self.lines = lines
                self.pos = 0
                self.line_num = 1

            def error(self, msg: str) -> None:
                """Выброс ошибки с указанием строки."""
                raise ValueError(f"Ошибка на строке {self.line_num}: {msg}")

            def parse(self) -> Dict[str, Any]:
                """Основной метод парсинга."""
                # Пропускаем XML-декларацию
                if self.content.startswith('<?xml'):
                    end = self.content.find('?>')
                    if end == -1:
                        self.error("Незакрытая XML-декларация")
                    self.pos = end + 2
                    self._update_line_num()

                self._skip_whitespace()
                if self.pos >= len(self.content) or self.content[self.pos] != '<':
                    self.error("Ожидался открывающий тег")

                tag, attrs, pos = self._parse_opening_tag()
                self.pos = pos
                result, self.pos = self._parse_element_content(tag, attrs)
                return {tag: result}

            def _update_line_num(self) -> None:
                """Обновление номера строки на основе позиции."""
                self.line_num = self.content[:self.pos].count('\n') + 1

            def _skip_whitespace(self) -> None:
                """Пропуск пробельных символов."""
                while self.pos < len(self.content) and self.content[self.pos] in ' \t\n\r':
                    if self.content[self.pos] == '\n':
                        self.line_num += 1
                    self.pos += 1

            def _parse_opening_tag(self) -> tuple:
                """Парсинг открывающего тега и его атрибутов."""
                if self.pos >= len(self.content) or self.content[self.pos] != '<':
                    self.error("Ожидался символ '<'")

                self.pos += 1
                start = self.pos
                while self.pos < len(self.content) and self.content[self.pos] not in ' >/':
                    self.pos += 1

                if start == self.pos:
                    self.error("Ожидалось имя тега")

                tag = self.content[start:self.pos]

                # Парсинг атрибутов
                attrs = {}
                while self.pos < len(self.content) and self.content[self.pos] != '>' and self.content[self.pos] != '/':
                    self._skip_whitespace()
                    if self.content[self.pos] == '>' or self.content[self.pos] == '/':
                        break

                    # Имя атрибута
                    attr_start = self.pos
                    while self.pos < len(self.content) and self.content[self.pos] not in ' =/>':
                        self.pos += 1
                    attr_name = self.content[attr_start:self.pos]

                    self._skip_whitespace()
                    if self.pos >= len(self.content) or self.content[self.pos] != '=':
                        self.error(f"Ожидался '=' после атрибута '{attr_name}'")
                    self.pos += 1

                    self._skip_whitespace()
                    if self.pos >= len(self.content) or self.content[self.pos] not in '"\'':
                        self.error("Ожидались кавычки вокруг значения атрибута")
                    quote = self.content[self.pos]
                    self.pos += 1

                    val_start = self.pos
                    while self.pos < len(self.content) and self.content[self.pos] != quote:
                        self.pos += 1
                    if self.pos >= len(self.content):
                        self.error("Незакрытые кавычки в значении атрибута")
                    attr_value = self.content[val_start:self.pos]
                    self.pos += 1

                    attrs[attr_name] = XMLSerializer._unescape_xml(attr_value)

                # Самозакрывающийся тег
                if self.pos < len(self.content) and self.content[self.pos] == '/':
                    self.pos += 1
                    if self.pos >= len(self.content) or self.content[self.pos] != '>':
                        self.error("Ожидался '>' после '/'")
                    self.pos += 1
                    return tag, attrs, self.pos

                if self.pos >= len(self.content) or self.content[self.pos] != '>':
                    self.error("Ожидался '>' в конце открывающего тега")
                self.pos += 1
                return tag, attrs, self.pos

            def _parse_element_content(self, tag: str, attrs: Dict) -> tuple:
                """Парсинг содержимого элемента."""
                self._skip_whitespace()
                content = ""
                children = {}
                current_tag = None

                while self.pos < len(self.content):
                    if self.content.startswith('</', self.pos):
                        # Закрывающий тег
                        close_pos = self.pos + 2
                        close_start = close_pos
                        while close_pos < len(self.content) and self.content[close_pos] != '>':
                            close_pos += 1
                        close_tag = self.content[close_start:close_pos]
                        if close_tag != tag:
                            self.error(f"Ожидался закрывающий тег </{tag}>, получен </{close_tag}>")
                        self.pos = close_pos + 1
                        self._update_line_num()
                        break

                    elif self.content.startswith('<?', self.pos):
                        # Пропуск инструкций
                        end = self.content.find('?>', self.pos)
                        if end == -1:
                            self.error("Незакрытая инструкция")
                        self.pos = end + 2
                        self._update_line_num()
                        continue

                    elif self.content.startswith('<!--', self.pos):
                        # Пропуск комментариев
                        end = self.content.find('-->', self.pos)
                        if end == -1:
                            self.error("Незакрытый комментарий")
                        self.pos = end + 3
                        self._update_line_num()
                        continue

                    elif self.content[self.pos] == '<':
                        # Открывающий тег дочернего элемента
                        child_tag, child_attrs, self.pos = self._parse_opening_tag()
                        child_data, self.pos = self._parse_element_content(child_tag, child_attrs)

                        if child_tag not in children:
                            children[child_tag] = child_data
                        else:
                            # Преобразование в список для нескольких элементов с одинаковым тегом
                            if not isinstance(children[child_tag], list):
                                children[child_tag] = [children[child_tag]]
                            children[child_tag].append(child_data)
                    else:
                        # Текстовое содержимое
                        text_start = self.pos
                        while self.pos < len(self.content) and self.content[self.pos] != '<':
                            if self.content[self.pos] == '\n':
                                self.line_num += 1
                            self.pos += 1
                        content += self.content[text_start:self.pos]

                content = content.strip()
                result = {}

                if attrs:
                    result["@attributes"] = attrs
                if children:
                    result.update(children)
                if content:
                    if children or attrs:
                        result["#text"] = XMLSerializer._unescape_xml(content)
                    else:
                        result = XMLSerializer._unescape_xml(content)

                return result if result else ("" if not children and not attrs else result), self.pos

        parser = XMLParser(xml_str, lines)
        return parser.parse()

    @staticmethod
    def validate(xml_str: str) -> bool:
        """
        Валидация XML-строки.

        Args:
            xml_str: XML-строка для проверки

        Returns:
            True если валиден, иначе False
        """
        try:
            XMLSerializer.deserialize(xml_str)
            print("XML валиден")
            return True
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return False

    @staticmethod
    def deserialize_file(filepath: str) -> Dict[str, Any]:
        """Десериализация XML из файла."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return XMLSerializer.deserialize(f.read())
        except FileNotFoundError:
            raise ValueError(f"Файл не найден: {filepath}")


# Демонстрация работы
def main():
    print("=" * 60)
    print("СЕРИАЛИЗАЦИЯ И ДЕСЕРИАЛИЗАЦИЯ XML")
    print("=" * 60)

    # Тестовые объекты
    test_objects = [
        # Простой объект
        {
            "person": {
                "@attributes": {"id": "123"},
                "name": "John Doe",
                "age": 30,
                "city": "New York"
            }
        },
        # Список однотипных элементов
        {
            "catalog": {
                "book": [
                    {"title": "XML Guide", "price": 19.99},
                    {"title": "Python Basics", "price": 29.99}
                ]
            }
        },
        # Смешанное содержимое
        {
            "description": {
                "#text": "This is a text with ",
                "bold": "bold",
                "#text2": " part."
            }
        }
    ]

    print("\n1. Сериализация в XML:")
    print("-" * 40)
    for i, obj in enumerate(test_objects, 1):
        print(f"\nТест {i}:")
        xml_str = XMLSerializer.serialize(obj, indent=2)
        print(xml_str)
        print("\nВалидация сгенерированного XML:")
        XMLSerializer.validate(xml_str)

    print("\n" + "=" * 60)
    print("2. Десериализация из XML:")
    print("-" * 40)

    xml_samples = [
        '<root><name>Alice</name><age>25</age><active>true</active></root>',
        '<library><book id="1">1984</book><book id="2">Brave New World</book></library>',
        '<response status="ok"><data><item>Value 1</item><item>Value 2</item></data></response>'
    ]

    for i, xml_str in enumerate(xml_samples, 1):
        print(f"\nТест {i}:")
        print(f"XML: {xml_str}")
        try:
            parsed = XMLSerializer.deserialize(xml_str)
            print(f"Результат: {parsed}")
            print("Валидация:", "✓" if XMLSerializer.validate(xml_str) else "✗")
        except ValueError as e:
            print(f"Ошибка: {e}")

    print("\n" + "=" * 60)
    print("3. Проверка на заведомо некорректных XML:")
    print("-" * 40)

    invalid_xmls = [
        '<root><name>Test</root>',
        '<root attr="value>',
        '<root><child></child></root',
        '<unclosed>text'
    ]

    for i, xml_str in enumerate(invalid_xmls, 1):
        print(f"\nНекорректный XML {i}: {xml_str}")
        XMLSerializer.validate(xml_str)

    print("\n" + "=" * 60)
    print("ГОТОВО")
    print("=" * 60)


if __name__ == "__main__":
    main()