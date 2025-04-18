# 🚀Прогресс Агро🚜 - автоматизация создания отчетов о полевых работах 🌿🌾🌻

![Прогресс Агро](https://github.com/OZheRelieV/AgroLLM_Hack/blob/main/assets/kandinsky-download-1744821581510.png)

# ⚠️ Проблематика и Решение ⚠️ 
Каждый день главному агроному стекается информация о проделанных работах на полях. Его задача - это проанализировать эту неструктурированную информацию, выделить релевантные части, а потом структурировать, заполнив excel таблицу.

Информация может быть представлена совершенно разным образом 🤔. Способ представления полностью зависит от агронома, который её присылает.  Это могут быть:
- сокращения до одной буквы, обозначающей часть культуры;
- пропуски в заполнении показателей за день;
- представление целевых показателей в процентах, а не в нужных единицах измерениях;
- пропуск и операции, и культуры, если они повторяются и т.д.

🔥 Всё это вносит сложность в анализе такого рода информации, поэтому нами был разработан сервис по анализу и структуризации информации, поступающей от агрономов, который:
- ❗ не меняет текущую логику отправки сообщений агрономами;
- ❗ автоматизирует процесс сбора и структурировании инфорамции;
- ❗ предоставляет возможность автоматического запуска сервиса с сохранением результатов работы, как на локальный диск, так и на google диск;
- ❗ требует намного меньше времени для работы, чем требуется главному агроному;
- ❗ обладает точностью более **95%** 🎯

Решение возможно запустить как на ОС Windows, так и на macOS / Linux. 

![Прогресс Агро](https://github.com/OZheRelieV/AgroLLM_Hack/blob/main/assets/service.png)

## ⚡Быстрый старт ⚡

### 🖥 Windows 🖥 

1. Откройте папку проекта 📁 и дважды кликните по **install.bat** 📄.
   - Если Python 🐍 не установлен — откроется страница загрузки. ❗❗❗ Установите Python , затем снова запустите `install.bat` ❗❗❗.
   - ⚠️ Все необходимые компоненты (Poetry, зависимости) установятся автоматически, окружение будет создано.
2. ▶️ Для запуска приложения дважды кликните по **start.bat** 📄.

### 🐧macOS / Linux 🐧

1. Откройте терминал в папке проекта и выполните ⌨️:
   ```sh
   ./install.sh
   ```
   - ❗❗❗ Если скрипт не запускается, дайте права: `chmod +x install.sh` ❗❗❗
   - ⚠️ Poetry и зависимости установятся автоматически, окружение будет создано.
2. ▶️Для запуска приложения выполните ⌨️:
   ```sh
   ./start.sh
   ```

---

## Использование приложения 🚀🚜💻


- 🧑‍💻 Для ручного создания отчёта перейдите на вкладку **📝 Ручной отчёт**, выберите дату и нажмите "Запустить анализ". Готовый Excel-файл 📄 можно скачать сразу из приложения.
- ⚙️ Для автоматического создания отчётов перейдите на вкладку **⏰ Автоматизация**:
  1. Выберите удобное время (часы и минуты).
  2. Нажмите "Включить автозапуск" — задача появится в планировщике Windows.
  3. В указанное время отчёт будет создаваться автоматически.
- 📊 Для просмотра графиков по отчётам используйте вкладку **📊 Визуализация**.
- 📝 Все отчёты сохраняются в папку **data/** внутри проекта.

---

## ❗❗❗ Важно ❗❗❗

- Для работы парсера необходим установленный Google Chrome.
- Не выключайте компьютер и не закрывайте браузер с авторизованным WhatsApp Web, если хотите, чтобы автозапуск работал корректно.

---

# Структура репозитория
📁 AgroLLM_Hack  
├─📁 app (папка с основными скриптами - запуск приложения, автозапуск)  
│ ├─📄 auto_report.py  
│ └─📄 run_auto_report.bat  
│ └─📄 run_auto_report.sh  
│ └─📄 streamlit_app.py  
├─📁 assets (папка со статическими элементами)  
│ └─📄 kandinsky-download-1744821581510.png  
│ └─📄 service.png  
├─📁 data (папка с данными)  
│ └─📄 abbreviations.json  
├─📁 llm_extraction (папка со скриптом экстракции информации из сообщений)  
│ └─📄 yandex_gpt_extraction.py  
├─📁 notebooks (папка с ноутбками (экстрация информации и оценка точности))  
│ └─📄 llm_extraction.ipynb  
│ └─📄 precision_estimation.ipynb (ноутбук для определения точности работы алгоритма)  
├─📁 testing_scripts (папка с тестовым скриптом)  
│ └─📄 save_messages_to_word.py  
├─📁 whatsapp_parser (папка со скриптом парсинга сообщений из WhatsApp)  
│ └─📄 wa_parser (1).py  
│ 📄 .env.example  
│ 📄 .gitignore  
│ 📄 README.md  
│ 📄 install.bat  
│ 📄 install.sh  
│ 📄 poetry.lock  
│ 📄 pyproject.toml  
│ 📄 start.bat  
│ 📄 start.sh  

# 🛠️ Технологический стек 🛠️ 

- 🐍 python 3.11
- 🐼 pandas
- 📄 openpyxl
- 🤖 selenium
- ⚙️ webdriver
- 🛠️ poetry
- 🧠 yandexgpt-lite
- 📋 structured output

Весь код оформлен по ❗**PEP 8**❗
