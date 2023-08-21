import datetime
import sqlite3
import aiocron
from aiogram import executor

from handlers.adjustment_handlers import adjustment_registry_handler
from handlers.apply_handlers import apply_handler
from handlers.user_handlers import adding_track_number_handler
from system.dispatcher import dp


def delete_yesterdays_records():
    try:
        # Подключиться к базе данных
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()

        # Получить вчерашнюю дату
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime("%d.%m")

        # Удалить записи с application_date, равным вчерашней дате
        cursor.execute("DELETE FROM reports WHERE application_date LIKE ?", (f"%{yesterday_str}%",))
        conn.commit()
        conn.close()

        print(f"Удаленные записи для{yesterday_str}")
    except Exception as e:
        print(f"Ошибка удаления записей: {e}")


def main():
    """Запуск бота с запланированным по времени удалением старых записей"""
    aiocron.crontab('0 0 * * *', delete_yesterdays_records)  # Запланированный запуск функции ежедневно в 00:00
    executor.start_polling(dp, skip_updates=True)
    apply_handler()  # Добавление трека
    adding_track_number_handler()  # Обработчик команды старт
    adjustment_registry_handler()  # Обработчик команды корректировки


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        print(e)
