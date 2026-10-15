import json
import re
from html.parser import HTMLParser

# НАСТРОЙКИ 
TC_TITLE_KEY = 'title'
STEPS_KEY = 'steps'
DESCRIPTION_KEY = 'description'
RESULT_KEY = 'result'
SECTIONS_KEY = 'sections'
CASES_KEY = 'cases'

# Глобальный счетчик тест-кейсов
test_case_counter = 0

# Список для сбора оглавления
toc_entries = []

class HTMLToTextParser(HTMLParser):
    #Парсит HTML и извлекает текст с базовым форматированием.#
    
    def __init__(self):
        super().__init__()
        self.result = []
        self.current_list = []
        self.in_list = False
        self.list_counter = 0
        
    def handle_starttag(self, tag, attrs):
        if tag in ['ol', 'ul']:
            self.in_list = True
            self.list_counter = 0
        elif tag == 'li':
            if self.in_list:
                self.list_counter += 1
                self.result.append(f"\n{self.list_counter}. ")
        elif tag == 'p':
            self.result.append("\n")
        elif tag == 'br':
            self.result.append("\n")
            
    def handle_endtag(self, tag):
        if tag in ['ol', 'ul']:
            self.in_list = False
            self.result.append("\n")
        elif tag == 'p':
            self.result.append("\n")
            
    def handle_data(self, data):
        self.result.append(data)
        
    def get_text(self):
        text = ''.join(self.result)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

def clean_html(html_text):
    #Конвертирует HTML в читаемый текст.
    if not html_text:
        return ''
    parser = HTMLToTextParser()
    parser.feed(html_text)
    return parser.get_text()

def get_next_test_id():
    #Возвращает следующий уникальный ID тест-кейса.
    global test_case_counter
    test_case_counter += 1
    return f"TC-{test_case_counter:03d}"

def process_section(section, lines, level=1):
    #Рекурсивно обрабатывает секцию (папку) и все вложенные секции.
    global toc_entries
    
    section_title = section.get(TC_TITLE_KEY, 'Без названия')
    
    # Добавляем заголовок папки в основной файл
    header_prefix = '#' * (level + 1)
    lines.append(f"{header_prefix} {section_title}\n")
    
    # Добавляем заголовок папки в оглавление
    toc_entries.append(f"{header_prefix} {section_title}\n")
    
    # Обрабатываем тест-кейсы в этой секции
    cases = section.get(CASES_KEY, [])
    for case in cases:
        case_title = case.get(TC_TITLE_KEY, 'Без названия')
        test_id = get_next_test_id()
        
        # Заголовок тест-кейса в основном файле
        lines.append(f"**[{test_id}] {case_title}**\n")
        
        # Добавляем тест-кейс в оглавление
        toc_entries.append(f"- **[{test_id}]** {case_title}\n")
        
        # Шаги
        steps = case.get(STEPS_KEY, [])
        if steps:
            for i, step in enumerate(steps, 1):
                description_html = step.get(DESCRIPTION_KEY, '')
                result_html = step.get(RESULT_KEY, '')
                
                description_text = clean_html(description_html)
                result_text = clean_html(result_html)
                
                if len(steps) > 1:
                    lines.append(f"*Шаг {i}:*\n")
                
                if description_text:
                    lines.append("**Действия:**")
                    lines.append(description_text + "\n")
                
                if result_text:
                    lines.append("**Ожидаемый результат:**")
                    lines.append(result_text + "\n")
                
                lines.append("")
        else:
            lines.append("_Шаги не описаны_\n")
        
        # Чекбокс
        lines.append("- [ ] Пройдено успешно\n")
        lines.append("<!-- Комментарии: -->\n")
        lines.append("---\n")
    
    # Рекурсивно обрабатываем вложенные секции
    nested_sections = section.get(SECTIONS_KEY, [])
    for nested_section in nested_sections:
        process_section(nested_section, lines, level + 1)

def generate_markdown(data):
    global test_case_counter, toc_entries
    test_case_counter = 0
    toc_entries = []
    
    lines = []
    lines.append("# Регрессионное тестирование\n")
    lines.append("---\n")
    
    # Обрабатываем все секции верхнего уровня
    sections = data.get(SECTIONS_KEY, [])
    for section in sections:
        process_section(section, lines, level=1)
    
    lines.insert(2, f"**Всего тест-кейсов:** {test_case_counter}\n")
    
    return "\n".join(lines), "\n".join(toc_entries)

def generate_toc(toc_content, total_cases):
    #Генерирует отдельный файл с оглавлением.#
    lines = []
    lines.append("# Оглавление\n")
    lines.append(f"**Всего тест-кейсов:** {total_cases}\n")
    lines.append("---\n")
    lines.append(toc_content)
    return "\n".join(lines)

INPUT_FILE = 'qwe.json'
OUTPUT_FILE = 'regression_checklist.md'
TOC_FILE = 'index.md'

print(f"Загружаю {INPUT_FILE}...")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Генерирую Markdown...")
markdown_content, toc_content = generate_markdown(data)

print(f"Сохраняю основной файл в {OUTPUT_FILE}...")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print(f"Сохраняю оглавление в {TOC_FILE}...")
toc_final = generate_toc(toc_content, test_case_counter)
with open(TOC_FILE, 'w', encoding='utf-8') as f:
    f.write(toc_final)

print(f"Готово! Всего тест-кейсов: {test_case_counter}")
print(f"Основной файл: {OUTPUT_FILE}")
print(f"Оглавление: {TOC_FILE}")