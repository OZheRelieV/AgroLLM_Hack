import os
import sys
from datetime import datetime
import subprocess
import pathlib
from dotenv import load_dotenv

# Определяем директории
script_path = pathlib.Path(__file__).resolve()
script_dir = script_path.parent
base_dir = script_dir.parent
DATA_DIR = base_dir / "data"

# Загружаем переменные окружения
env_path = base_dir / '.env'
load_dotenv(env_path)

yandex_key = os.getenv('YANDEX_API_KEY')
yandex_folder = os.getenv('YANDEX_FOLDER_ID')
chat_name = os.getenv('CHAT_NAME')

if not (yandex_key and yandex_folder and chat_name):
    print("[ERROR] Не заданы все переменные окружения (YANDEX_API_KEY, YANDEX_FOLDER_ID, CHAT_NAME)")
    sys.exit(1)

# Получаем дату для отчёта (по умолчанию сегодня)
if len(sys.argv) > 1:
    try:
        manual_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    except Exception:
        print("[ERROR] Формат даты: YYYY-MM-DD")
        sys.exit(1)
else:
    manual_date = datetime.now().date()

dt_str = f"{manual_date.strftime('%Y-%m-%d')} 00:00"
date_str = manual_date.strftime('%d-%m-%Y')
dated_excel = DATA_DIR / f"{date_str}.xlsx"
chat_json = DATA_DIR / f"chat_messages_{date_str}.json"

# 1. Запуск парсера WhatsApp
parser_cmd = [
    sys.executable, str(base_dir / "whatsapp_parser" / "wa_parser.py"), dt_str
]
print(f"[INFO] Запуск парсера: {' '.join(parser_cmd)}")
result1 = subprocess.run(parser_cmd, capture_output=True, text=True)
if result1.returncode != 0:
    print("[ERROR] Ошибка при парсинге WhatsApp:")
    print(result1.stderr)
    sys.exit(1)
if not chat_json.exists():
    print("[WARNING] Нет сообщений за выбранную дату. Файл не создан.")
    sys.exit(0)
print(f"[INFO] Сообщения собраны: {chat_json.name}")

# 2. Запуск анализатора (LLM)
model_local = "yandex_gpt_extraction"
script = base_dir / "llm_extraction" / f"{model_local}.py"
analyzer_cmd = [
    sys.executable, str(script), "--input", str(chat_json), "--output", str(dated_excel)
]
print(f"[INFO] Запуск анализатора: {' '.join(analyzer_cmd)}")
result2 = subprocess.run(analyzer_cmd, capture_output=True, text=True)
if result2.returncode != 0:
    print("[ERROR] Ошибка при анализе сообщений:")
    print(result2.stderr)
    sys.exit(1)
if not dated_excel.exists():
    print("[WARNING] Excel-файл не был создан после анализа.")
    sys.exit(0)
print(f"[SUCCESS] Excel-отчёт готов: {dated_excel}") 