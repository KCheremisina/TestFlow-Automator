import pypandoc #   py -m pip install pypandoc_binary
import os
import sys

def convert_md_to_docx(md_file_path, docx_file_path=None):
    #Конвертирует Markdown файл в Word (docx).
    if not os.path.exists(md_file_path):
        print(f"Ошибка: Файл '{md_file_path}' не найден.")
        return

    if docx_file_path is None:
        base_name = os.path.splitext(md_file_path)[0]
        docx_file_path = f"{base_name}.docx"

    try:
        print(f"Начинаю конвертацию '{md_file_path}' -> '{docx_file_path}'...")
        
        pypandoc.convert_file(
            md_file_path, 
            'docx', 
            outputfile=docx_file_path
        )
        
        print(f"Успешно! Файл сохранен: {os.path.abspath(docx_file_path)}")
        
    except OSError as e:
        print("Ошибка: Не удалось найти Pandoc.")
        print(f"Детали ошибки: {e}")
    except Exception as e:
        print(f"Произошла ошибка при конвертации: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_file = "textMD.md" 
        output_file = "document.docx"

    convert_md_to_docx(input_file, output_file)