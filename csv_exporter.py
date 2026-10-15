import re
import csv
from datetime import datetime

INPUT_FILE = 'index.md'
OUTPUT_FILE = 'test_report.csv'

def parse_index(filepath):
    #Парсит index.md и извлекает структуру тестов.
    test_cases = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    folder_path = []  
    
    for line in lines:
        line = line.strip()
        
        if not line or line.startswith('# Оглавление') or line.startswith('**Всего') or line == '---':
            continue
    
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            
            if level <= len(folder_path):
                folder_path = folder_path[:level-1]
            folder_path.append(title)
            
            continue
        
        if line.startswith('- **['):
            match = re.search(r'\*\*\[(TC-\d+)\]\*\*\s*(.+)', line)
            if match:
                test_id = match.group(1)
                test_title = match.group(2)
                
                test_cases.append({
                    'id': test_id,
                    'folder': ' > '.join(folder_path),
                    'title': test_title,
                    'status': '',
                    'comments': '',
                    'last_run': ''
                })
    
    return test_cases

def export_to_csv(test_cases, filepath):
    #Экспортирует тест-кейсы в CSV файл.
    if not test_cases:
        print("Нет тест-кейсов для экспорта!")
        return
    
    with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'folder', 'title', 'status', 'comments', 'last_run'])
        writer.writeheader()
        writer.writerows(test_cases)

print(f"Парсю {INPUT_FILE}...")
test_cases = parse_index(INPUT_FILE)

print(f"Найдено тест-кейсов: {len(test_cases)}")

if test_cases:
    print(f"Экспортирую в {OUTPUT_FILE}...")
    export_to_csv(test_cases, OUTPUT_FILE)
    print(f"Готово! Открой {OUTPUT_FILE} в Excel.")
    print("\nСтруктура файла:")
    print("- id: ID теста (TC-001, TC-002, ...)")
    print("- folder: Путь к папке (Папка > Подпапка > ...)")
    print("- title: Название теста")
    print("- status: Пустое поле для заполнения (Pass/Fail/Blocked)")
    print("- comments: Пустое поле для комментариев")
    print("- last_run: Пустое поле для даты последнего прохождения")
else:
    print("Не удалось распарсить тест-кейсы. Проверь формат index.md.")