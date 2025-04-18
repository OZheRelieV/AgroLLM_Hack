import os
import pathlib
import platform
import subprocess
import sys
from datetime import date, datetime, time

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv, set_key

st.set_page_config(page_title="AgroLLM", layout="wide")

# --- Стили ---
st.markdown(
    """
<style>
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2em;
        color: #2E7D32;
    }
    .stButton > button, .stDownloadButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 1.1em !important;
        padding: 0.5em 1.5em !important;
        margin-bottom: 0.5em;
        transition: background 0.2s;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #388e3c !important;
        color: #fff !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- Заголовок ---
st.markdown(
    """
<h1 style='text-align: center; color: #2E7D32; font-size: 2.8em; margin-bottom: 0.2em;'>Прогресс Агро</h1>
<p style='text-align: center; color: #555; font-size: 1.3em; margin-top: 0;'>автоматизация создания отчетов о полевых работах</p>
<hr style='margin-bottom: 2em;'>
""",
    unsafe_allow_html=True,
)

# --- Директории и переменные ---
script_path = pathlib.Path(__file__).resolve()
script_dir = script_path.parent
base_dir = script_dir.parent
DATA_DIR = base_dir / "data"
env_path = base_dir / ".env"
load_dotenv(env_path)

yandex_key = os.getenv("YANDEX_API_KEY")
yandex_folder = os.getenv("YANDEX_FOLDER_ID")
chat_name = os.getenv("CHAT_NAME")

# --- Вкладки ---
tabs = st.tabs(
    [
        "📝 Ручной отчёт",
        "⏰ Автоматизация",
        "📊 Визуализация",
        "ℹ️ Инструкция",
        "⚙️ Настройки",
    ]
)

# --- 1. Ручной отчёт ---
with tabs[0]:
    st.markdown(
        """
    <h2 style='color:#2E7D32;'>📝 Ручной запуск отчёта</h2>
    <p>Выберите дату и получите Excel-отчёт по WhatsApp-чату.</p>
    """,
        unsafe_allow_html=True,
    )
    default_manual_date = datetime.now().date()
    manual_date = st.date_input(
        "Дата отчёта", value=default_manual_date, key="manual_date"
    )
    if st.button("Запустить анализ", type="primary"):
        try:
            dt_str = f"{manual_date.strftime('%Y-%m-%d')} 00:00"
            date_str = manual_date.strftime("%d-%m-%Y")
            dated_excel = DATA_DIR / f"{date_str}.xlsx"
            chat_json = DATA_DIR / f"chat_messages_{date_str}.json"
            with st.spinner(
                f"Парсинг и анализ WhatsApp за {manual_date.strftime('%d.%m.%Y')}..."
            ):
                parser_cmd = [
                    "poetry",
                    "run",
                    "python",
                    str(base_dir / "whatsapp_parser" / "wa_parser.py"),
                    dt_str,
                ]
                result1 = subprocess.run(parser_cmd, capture_output=True, text=True)
                if result1.returncode != 0:
                    st.error(
                        "Ошибка при парсинге сообщений WhatsApp. Проверьте настройки и повторите попытку."
                    )
                elif not chat_json.exists():
                    st.warning("Нет сообщений за выбранную дату. Файл не создан.")
                else:
                    st.success(
                        f"Сообщения успешно собраны! Использован файл: {chat_json.name}\nЗапускается анализ..."
                    )
                    model_local = "yandex_gpt_extraction"
                    script = base_dir / "llm_extraction" / f"{model_local}.py"
                    analyzer_cmd = [
                        "python",
                        str(script),
                        "--input",
                        str(chat_json),
                        "--output",
                        str(dated_excel),
                    ]
                    result2 = subprocess.run(
                        analyzer_cmd, capture_output=True, text=True
                    )
                    if result2.returncode != 0:
                        st.error(
                            "Ошибка при анализе сообщений и формировании Excel-файла. Проверьте корректность данных."
                        )
                    elif not dated_excel.exists():
                        st.warning(
                            "Excel-файл не был создан после анализа. Проверьте корректность исходных данных."
                        )
                    else:
                        st.success(f"Excel-файл готов: {date_str}.xlsx")
                        with open(dated_excel, "rb") as f:
                            st.download_button(
                                f"Скачать {date_str}.xlsx",
                                f,
                                file_name=f"{date_str}.xlsx",
                                type="primary",
                            )
                        try:
                            df = pd.read_excel(dated_excel)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        except Exception as e:
                            st.warning(
                                "Excel-файл создан, но не удалось отобразить его содержимое."
                            )
        except Exception as exc:
            st.exception(exc)

# --- 2. Автоматизация ---
with tabs[1]:
    st.markdown(
        """
    <h2 style='color:#2E7D32;'>⏰ Автоматизация (автозапуск)</h2>
    <p>Настройте автоматический запуск отчёта по расписанию (только для Windows).</p>
    """,
        unsafe_allow_html=True,
    )
    if platform.system() != "Windows":
        st.info("Автозапуск через планировщик задач доступен только на Windows.")
    else:
        auto_time = st.time_input(
            "Время автозапуска (часы:минуты)",
            value=time(23, 59),
            key="auto_time",
            step=60,
        )
        enable = st.button("Включить автозапуск", key="enable_autorun")
        disable = st.button("Отключить автозапуск", key="disable_autorun")
        task_name = "AgroLLM_AutoReport"
        bat_path = str((base_dir / "app" / "run_auto_report.bat").resolve())
        st.markdown(
            f"Скрипт для ручного запуска: <code>{bat_path}</code>",
            unsafe_allow_html=True,
        )
        if enable:
            hour, minute = auto_time.hour, auto_time.minute
            cmd = (
                f'schtasks /Create /F /SC DAILY /TN "{task_name}" '
                f'/TR "{bat_path}" '
                f"/ST {hour:02d}:{minute:02d}"
            )
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                st.success(
                    "Автозапуск успешно настроен! Задача появится в планировщике Windows."
                )
            else:
                st.error(f"Ошибка при настройке автозапуска: {result.stderr}")
        if disable:
            cmd = f'schtasks /Delete /F /TN "{task_name}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                st.success(
                    "Автозапуск отключён. Задача удалена из планировщика Windows."
                )
            else:
                st.error(f"Ошибка при удалении задачи: {result.stderr}")

# --- 3. Визуализация ---
with tabs[2]:
    st.markdown(
        """
    <h2 style='color:#2E7D32;'>📊 Визуализация отчётов</h2>
    <p>Графики по подразделениям и операциям на основе последних отчётов.</p>
    """,
        unsafe_allow_html=True,
    )
    if st.checkbox("Показать графики по подразделениям и операциям", value=False):
        try:
            excel_files = [f for f in DATA_DIR.iterdir() if f.suffix == ".xlsx"]
            if excel_files:
                latest_file = max(excel_files, key=lambda x: x.stat().st_mtime)
                df = pd.read_excel(latest_file)
                st.info(f"Визуализация по файлу: {latest_file.name}")
                df = df.dropna(
                    subset=["Подразделение", "Операция", "Культура", "За день (га)"]
                )
                df = df[df["За день (га)"].astype(str).str.strip() != ""]
                for podrazdelenie in df["Подразделение"].unique():
                    st.markdown(
                        f"<h4 style='color:#388e3c;'>{podrazdelenie}</h4>",
                        unsafe_allow_html=True,
                    )
                    df_podr = df[df["Подразделение"] == podrazdelenie]
                    for oper in df_podr["Операция"].unique():
                        df_oper = df_podr[df_podr["Операция"] == oper]
                        data = (
                            df_oper.groupby("Культура")["За день (га)"]
                            .apply(lambda x: pd.to_numeric(x, errors="coerce").sum())
                            .reset_index()
                        )
                        fig = px.bar(
                            data,
                            x="Культура",
                            y="За день (га)",
                            title=f"{oper}",
                            labels={"За день (га)": "Гектаров за день"},
                            color="Культура",
                        )
                        st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Ошибка визуализации: {e}")

# --- 4. Инструкция ---
with tabs[3]:
    st.markdown(
        """
    <h2 style='color:#2E7D32;'>ℹ️ Инструкция для пользователя</h2>
    <ul>
        <li>Перейдите на вкладку <b>📝 Ручной отчёт</b>, выберите дату и нажмите <b>Запустить анализ</b>. После завершения анализа скачайте Excel-файл с результатами.</li>
        <li>Для автоматического создания отчётов перейдите на вкладку <b>⏰ Автоматизация</b>, выберите время и включите автозапуск.</li>
        <li>Для просмотра графиков по отчётам используйте вкладку <b>📊 Визуализация</b>.</li>
        <li>Все отчёты сохраняются в папку <b>data/</b> внутри проекта.</li>
    </ul>
    """,
        unsafe_allow_html=True,
    )

# --- 5. Настройки ---
with tabs[4]:
    load_dotenv(env_path, override=True)
    chat_name = os.getenv("CHAT_NAME")
    yandex_key = os.getenv("YANDEX_API_KEY")
    yandex_folder = os.getenv("YANDEX_FOLDER_ID")
    st.markdown(
        """
    <h2 style='color:#2E7D32;'>⚙️ Настройки</h2>
    <p>Измените параметры для работы приложения. После сохранения страница обновится автоматически.</p>
    """,
        unsafe_allow_html=True,
    )
    chat_name_new = st.text_input(
        "Название чата WhatsApp", value=chat_name or "", key="settings_chat_name"
    )
    yandex_key_new = st.text_input(
        "Yandex API Key", value=yandex_key or "", key="settings_yandex_key"
    )
    yandex_folder_new = st.text_input(
        "Yandex Folder ID", value=yandex_folder or "", key="settings_yandex_folder"
    )
    if st.button("Сохранить настройки", type="primary"):
        if not (chat_name_new and yandex_key_new and yandex_folder_new):
            st.error("Пожалуйста, заполните все поля для сохранения настроек.")
            st.stop()
        set_key(str(env_path), "CHAT_NAME", chat_name_new)
        set_key(str(env_path), "YANDEX_API_KEY", yandex_key_new)
        set_key(str(env_path), "YANDEX_FOLDER_ID", yandex_folder_new)
        st.success(
            "Настройки успешно сохранены!"
        )
        st.stop()
