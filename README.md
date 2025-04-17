# Прогресс Агро — автоматизация создания отчетов о полевых работах

## Инструкция по установке и запуску (Windows)

### 1. Установка

1. Скачайте архив с проектом и распакуйте его в удобную папку на компьютере.
2. Откройте эту папку и дважды кликните по файлу **install.bat**.
   - Если Python не установлен — откроется страница загрузки. Установите Python, затем снова запустите `install.bat`.
   - Все необходимые компоненты (Poetry, зависимости) установятся автоматически.
3. Дождитесь сообщения "Установка завершена!" и нажмите любую клавишу для закрытия окна.

### 2. Первый запуск

1. Дважды кликните по файлу **start.bat**.
2. Откроется окно браузера с приложением "Прогресс Агро".
3. При первом запуске:
   - Заполните настройки: введите API-ключи и название чата WhatsApp.
   - Откройте WhatsApp Web (в браузере появится окно авторизации).
   - Отсканируйте QR-код с помощью приложения WhatsApp на телефоне (как при обычной авторизации WhatsApp Web).

### 3. Использование

- Для ручного создания отчёта перейдите на вкладку **📝 Ручной отчёт**, выберите дату и нажмите "Запустить анализ". Готовый Excel-файл можно скачать сразу из приложения.
- Для автоматического создания отчётов перейдите на вкладку **⏰ Автоматизация**:
  1. Выберите удобное время (часы и минуты).
  2. Нажмите "Включить автозапуск" — задача появится в планировщике Windows.
  3. В указанное время отчёт будет создаваться автоматически.
- Для просмотра графиков по отчётам используйте вкладку **📊 Визуализация**.
- Все отчёты сохраняются в папку **data/** внутри проекта.

### 4. Важно

- Для работы парсера необходим установленный Google Chrome.
- Не выключайте компьютер и не закрывайте браузер с авторизованным WhatsApp Web, если хотите, чтобы автозапуск работал корректно.

