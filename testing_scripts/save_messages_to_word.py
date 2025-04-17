import json
import pathlib
import sys
from datetime import datetime

from docx import Document

# === Настройки ===
TEAM_NAME = "Немезида"
INPUT_JSON = sys.argv[1] if len(sys.argv) > 1 else "../data/chat_messages.json"
OUTPUT_DIR = pathlib.Path(f"../testing_output/{TEAM_NAME}")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    messages = json.load(f)

sender_msg_count = {}

for i, msg in enumerate(messages, 1):
    author = msg.get("author", "Unknown")
    text = msg.get("text", "")
    date_str = msg.get("date", "")
    # Для уникальности: если несколько сообщений от одного автора
    sender_msg_count.setdefault(author, 0)
    sender_msg_count[author] += 1
    msg_number = sender_msg_count[author]
    # Формируем дату для имени файла
    now = datetime.now()
    if date_str:
        try:
            # Если дата есть, используем её, иначе - текущую
            now = datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            pass
    file_time = now.strftime("%M%H%d%m%Y")
    safe_author = author.replace(" ", "_").replace("/", "_")
    filename = f"{safe_author}_{msg_number}_{file_time}.docx"
    filepath = OUTPUT_DIR / filename
    # Сохраняем в Word
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filepath)
    print(f"Сохранено: {filepath}")
