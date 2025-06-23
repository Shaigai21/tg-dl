import json
from typing import Any

def read_json_file(file_path: str) -> Any | None:
    """
    Читает и возвращает данные из JSON-файла.

    Параметры:
        file_path (str): Путь к JSON-файлу

    Возвращает:
        Any | None: Данные из файла в формате Python или None при ошибке
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
            
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: JSON file '{file_path}' corrupted.")
    except UnicodeDecodeError:
        print(f"Error: wrong file encoding '{file_path}'.")
    except Exception as e:
        print(f"Error {e}")
    
    return None

