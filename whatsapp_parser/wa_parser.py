from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
from datetime import datetime, timedelta
import sys
from dotenv import load_dotenv
import pathlib

load_dotenv(override=True)

# --- Функция для запроса и парсинга даты/времени ---
def get_datetime_input(prompt):
    """Запрашивает у пользователя дату и время в формате YYYY-MM-DD HH:MM
       и возвращает объект datetime. Если пользователь ничего не вводит, возвращает сегодняшнюю дату с 00:00."""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    default = f"{today} 00:00"
    while True:
        dt_str = input(f"{prompt} (формат ГГГГ-ММ-ДД ЧЧ:ММ, Enter — сегодня с 00:00): ")
        if not dt_str.strip():
            return datetime.strptime(default, "%Y-%m-%d %H:%M")
        try:
            dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            return dt_obj
        except ValueError:
            print("Неверный формат. Пожалуйста, используйте формат ГГГГ-ММ-ДД ЧЧ:ММ или просто Enter.")

# --- Запрос диапазона у пользователя ---
print("Укажите дату и время начала парсинга сообщений.")
if len(sys.argv) > 1:
    try:
        start_datetime = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M")
        print(f"Используется дата из аргумента: {start_datetime}")
        date_for_filename = start_datetime.strftime('%d-%m-%Y')
    except Exception as e:
        print(f"Ошибка разбора даты из аргумента: {e}. Будет использован интерактивный ввод.")
        start_datetime = get_datetime_input("Введите начальную дату и время")
        date_for_filename = start_datetime.strftime('%d-%m-%Y')
else:
    start_datetime = get_datetime_input("Введите начальную дату и время")
    date_for_filename = start_datetime.strftime('%d-%m-%Y')
end_datetime = start_datetime + timedelta(days=1)

# Дата и время парсинга для имени файла
parse_datetime_str = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

print(f"Парсинг сообщений начиная с {start_datetime}")

# --- Настройки драйвера ---
options = webdriver.ChromeOptions()
# Раскомментируйте и настройте путь, если хотите использовать существующий профиль
options.add_argument("--user-data-dir=./chrome_profile") # Замените путь
options.add_argument("--profile-directory=Default") # Или Profile 1, Profile 2 и т.д.
#options.add_argument("--user-data-dir=./user_profile") # Используем локальную папку для профиля
#options.add_argument("--profile-directory=Default")
options.add_argument("--lang=ru-RU") # Попробуем установить язык интерфейса

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
except Exception as e:
    print(f"Ошибка инициализации драйвера: {e}")
    print("Убедитесь, что Chrome установлен и webdriver-manager может скачать драйвер.")
    exit()

# URL WhatsApp Web
URL = "https://web.whatsapp.com/"
CHAT_NAME = os.getenv("CHAT_NAME")  

# --- Открываем WhatsApp Web ---
driver.get(URL)
print("Ожидание загрузки WhatsApp Web и авторизации...")
# Ждем появления поля поиска чатов (или другого уникального элемента)
search_box_xpath = "//div[@contenteditable='true'][@data-tab='3']"
try:
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, search_box_xpath))
    )
    print("WhatsApp Web загружен, продолжаем...")
except TimeoutException:
    print("Не удалось дождаться загрузки WhatsApp Web. Проверьте авторизацию и интернет.")
    driver.quit()
    exit()

# --- Открываем указанный чат ---
try:
    print(f"Поиск чата '{CHAT_NAME}'...")
    # Ожидание появления поля поиска чатов
    search_box_xpath = "//div[@contenteditable='true'][@data-tab='3']"
    search_box = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, search_box_xpath))
    )
    search_box.click()
    search_box.send_keys(CHAT_NAME)
    time.sleep(2) # Даем время на фильтрацию списка чатов

    # Ищем чат в результатах поиска
    chat_xpath = f"//span[@title='{CHAT_NAME}']"
    chat = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, chat_xpath))
    )
    # Скроллим к элементу
    driver.execute_script("arguments[0].scrollIntoView(true);", chat)
    time.sleep(1)  # Даем время на анимацию
    # Пробуем обычный клик
    try:
        chat.click()
    except Exception:
        # Если не получилось — пробуем кликнуть через JS
        driver.execute_script("arguments[0].click();", chat)
    print(f"Чат '{CHAT_NAME}' успешно открыт.")
    time.sleep(2) # Даем время на загрузку сообщений чата

except TimeoutException:
    print(f"Ошибка: Чат с названием '{CHAT_NAME}' не найден или не загрузился вовремя.")
    print("Возможные причины: неверное название чата, медленное интернет-соединение, изменения в интерфейсе WhatsApp.")
    driver.quit()
    exit()
except Exception as e:
    print(f"Непредвиденная ошибка при открытии чата: {e}")
    driver.quit()
    exit()

# --- Парсим сообщения ---
messages = []
try:
    print("Загрузка истории сообщений...")
    # Ожидание загрузки области сообщений (используем более общий XPath)
    chat_box_xpath = "//div[contains(@class, 'copyable-area')]//div[@role='application']"
    chat_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, chat_box_xpath))
    )
    actions = ActionChains(driver)

    # Прокручиваем вверх для загрузки старых сообщений
    # Количество прокруток может потребоваться увеличить для очень длинных чатов
    # или если искомый диапазон находится далеко в прошлом.
    scroll_attempts = 20 # Увеличиваем количество попыток прокрутки
    print(f"Прокрутка вверх ({scroll_attempts} раз) для загрузки истории. Это может занять время...")
    for i in range(scroll_attempts):
        # Используем HOME вместо PAGE_UP для более быстрой прокрутки к началу
        chat_box.send_keys(Keys.HOME)
        # actions.key_down(Keys.CONTROL).send_keys(Keys.HOME).key_up(Keys.CONTROL).perform() # Альтернативный способ
        time.sleep(0.6) # Небольшая пауза между прокрутками
        if i % 10 == 0:
            print(f"Прокрутка {i}/{scroll_attempts}...")

    print("Загрузка истории завершена. Начинаем парсинг сообщений...")
    time.sleep(3) # Даем время элементам стабилизироваться после прокрутки

    # Ищем все элементы сообщений (входящие и исходящие)
    message_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in') or contains(@class, 'message-out')]")
    print(f"Найдено {len(message_elements)} элементов сообщений для анализа.")

    found_first_relevant_message = False # Флаг, что мы вошли в нужный диапазон
    processed_count = 0
    added_count = 0

    # Итерируем по найденным сообщениям (обычно они идут от старых к новым в DOM после прокрутки вверх)
    for i, msg in enumerate(message_elements):
        try:
            # Извлекаем атрибут с датой, временем и автором
            timestamp_attr = msg.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]").get_attribute("data-pre-plain-text")

            if not timestamp_attr: # Пропускаем элементы без этой информации (например, системные сообщения "Сообщение удалено")
                continue

            # Парсим дату и время из атрибута "[ЧЧ:ММ, ДД.ММ.ГГГГ] Автор:"
            # Формат может немного отличаться в зависимости от языка/версии WA
            try:
                # Извлекаем часть с датой/временем
                dt_part = timestamp_attr.split('[', 1)[1].split(']', 1)[0]
                msg_datetime = None # Инициализируем переменную для даты/времени

                # --- Пытаемся распознать формат с ТОЧКАМИ (ДД.ММ.ГГГГ) ---
                try:
                    msg_datetime = datetime.strptime(dt_part, "%H:%M, %d.%m.%Y")
                except ValueError:
                    # --- Если не получилось, пытаемся распознать формат со СЛЭШАМИ (Д/ММ/ГГГГ) ---
                    try:
                        msg_datetime = datetime.strptime(dt_part, "%H:%M, %d/%m/%Y")
                    except ValueError:
                        # --- Если ОБА формата не подошли, вызываем ошибку, которую поймает внешний except ---
                        # Это гарантирует, что мы не продолжим без правильно распознанной даты
                        raise ValueError(f"time data '{dt_part}' does not match known formats")

                # --- Если дата успешно распознана одним из способов ---
                time_sent_str = msg_datetime.strftime("%H:%M:%S") # Время для сохранения
                date_sent_str = msg_datetime.strftime("%Y-%m-%d") # Дата для сохранения

                # Извлекаем автора (после успешного парсинга даты)
                author = timestamp_attr.split('] ', 1)[-1].split(':')[0].strip()

            except (IndexError, ValueError) as dt_parse_error:
                # Этот блок теперь сработает, если не удалось извлечь dt_part
                # ИЛИ если НИ ОДИН из форматов даты не подошел
                print(f"Предупреждение: Не удалось распарсить дату/время/автора из '{timestamp_attr}'. Пропуск сообщения. Ошибка: {dt_parse_error}")
                continue

            processed_count += 1

            # --- Логика фильтрации по дате/времени ---
            if msg_datetime < start_datetime:
                continue
            elif msg_datetime >= end_datetime:
                continue
            else:
                found_first_relevant_message = True

                # Извлекаем текст сообщения
                text = ""
                try:
                    # Ищем основной контейнер текста
                    text_wrapper = msg.find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]")
                    # Внутри него могут быть вложенные span для эмодзи, ссылок и т.д.
                    inner_spans = text_wrapper.find_elements(By.XPATH, ".//span")
                    if inner_spans:
                         # Собираем текст из всех вложенных span, если они есть
                         # Это помогает собрать текст, разделенный эмодзи или форматированием
                        text = "".join([el.text for el in inner_spans])
                    else:
                        # Если вложенных span нет, берем текст из родительского span
                        text = text_wrapper.text

                    # Если текст все еще пуст, попробуем другой XPath (на случай медиа с подписью)
                    if not text:
                       caption_element = msg.find_elements(By.XPATH, ".//span[@data-testid='caption']")
                       if caption_element:
                           text = caption_element[0].text

                except NoSuchElementException:
                    # Может быть сообщение без текста (только медиа без подписи)
                    text = "[Медиа без текста или другое нетекстовое сообщение]"
                except StaleElementReferenceException:
                    print("Предупреждение: Элемент сообщения устарел во время извлечения текста. Пропуск.")
                    continue
                except Exception as text_exc:
                     print(f"Предупреждение: Не удалось извлечь текст сообщения. Ошибка: {text_exc}")
                     text = "[Ошибка извлечения текста]"


                messages.append({
                    "text": text.strip(), # Убираем лишние пробелы по краям
                    "author": author,
                    "date": date_sent_str,
                    "time": time_sent_str,
                    "timestamp": f"[{dt_part}] {author}:",
                    "datetime_obj": msg_datetime.isoformat() # Сохраняем для возможной доп. обработки
                })
                added_count += 1
                # print(f"Добавлено сообщение от {author} ({date_sent_str} {time_sent_str})") # Отладка

        except StaleElementReferenceException:
            print(f"Предупреждение: Элемент сообщения {i+1} устарел (StaleElementReferenceException). Пропуск.")
            continue # Пропускаем этот элемент и переходим к следующему
        except NoSuchElementException as e:
            # Иногда структура сообщения может отличаться (опросы, реакции и т.д.)
             print(f"Предупреждение: Не найден ожидаемый элемент в структуре сообщения {i+1}. Возможно, это не стандартное сообщение. Ошибка: {e}. Пропуск.")
             continue
        except Exception as e:
            print(f"Ошибка при обработке сообщения {i+1}: {e}")
            # Можно добавить traceback для детальной отладки:
            # import traceback
            # print(traceback.format_exc())

    print(f"Анализ завершен. Обработано сообщений: {processed_count}. Добавлено в файл: {added_count}.")

    # --- Сохраняем сообщения в JSON ---
    if messages:
        # Сортируем сообщения по дате/времени перед сохранением (на всякий случай)
        messages.sort(key=lambda x: datetime.fromisoformat(x['datetime_obj']))
        # Оставляем только нужные поля
        result = [
            {
                'author': msg['author'],
                'date': msg['date'],
                'text': msg['text']
            }
            for msg in messages
        ]
        # Работа с путями через pathlib
        script_path = pathlib.Path(__file__).resolve()
        script_dir = script_path.parent
        data_dir = script_dir.parent / "data"
        data_dir.mkdir(exist_ok=True)
        output_filename = data_dir / f"chat_messages_{date_for_filename}.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"Сообщения за указанный период успешно сохранены в {output_filename}")
    else:
        print("В указанном диапазоне дат/времени сообщений не найдено или не удалось их обработать.")

except TimeoutException as e:
    print(f"Ошибка ожидания элемента: {e}")
    print("Возможно, страница не загрузилась полностью или структура WhatsApp Web изменилась.")
except Exception as e:
    print(f"Произошла ошибка во время парсинга сообщений: {e}")
    # import traceback
    # print(traceback.format_exc()) # Раскомментируйте для детальной отладки

finally:
    print("Завершение работы скрипта.")
    if 'driver' in locals() and driver:
        driver.quit()
