import sqlite3

from aiogram import types

from keyboards.adjustment_keyboards import adjustment_keyboard
from system.dispatcher import bot
from system.dispatcher import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class YourState(StatesGroup):
    ID_INPUT = State()


@dp.callback_query_handler(lambda c: c.data == 'correction_of_reports_key')
async def adjustment_record_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Выбор варианта корректировки"""
    await state.finish()
    await state.reset_state()  # Сброс состояния
    greeting_post = ("Выберите нужное действие для удаления ❌ не корректной записи в отчете 📝.\n\n\n"
                     "<b>Для возврата 🔙 в начало нажмите</b> /start")
    adjustment_key = adjustment_keyboard()  # Клавиатура корректировки состояния
    # Получить идентификатор чата из callback_query
    chat_id = callback_query.message.chat.id
    # Отправьте сообщение в чат, используя полученный chat_id
    await bot.send_message(chat_id, greeting_post, reply_markup=adjustment_key, disable_web_page_preview=True,
                           parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data == 'for_tomorrow_key')
async def adjustment_record_for_tomorrow_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Корректировка отчета на завтра"""
    await state.finish()
    await state.reset_state()
    greeting_post = ("Введите ID записи для удаления не корректной записи в отчете 📝 НА ЗАВТРА 🗓.\n\n\n"
                     "<b>Для возврата 🔙 в начало нажмите</b> /start")
    await bot.send_message(callback_query.from_user.id, greeting_post)
    await YourState.ID_INPUT.set()  # Переход к ожиданию ввода ID


@dp.callback_query_handler(lambda c: c.data == 'today_key')
async def adjustment_record_for_tomorrow_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Корректировка отчета на завтра"""
    await state.finish()
    await state.reset_state()
    greeting_post = ("Введите ID записи для удаления не корректной записи в отчете 📝 ЗА СЕГОДНЯ 🗓.\n\n\n"
                     "<b>Для возврата 🔙 в начало нажмите</b> /start")
    await bot.send_message(callback_query.from_user.id, greeting_post)
    await YourState.ID_INPUT.set()  # Переход к ожиданию ввода ID


@dp.message_handler(state=YourState.ID_INPUT)
async def process_record_update(message: types.Message, state: FSMContext):
    try:
        record_id = int(message.text)
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()

        # Проверяем, существует ли запись с указанным ID
        cursor.execute(f"SELECT * FROM reports WHERE id_number = {record_id}")
        record = cursor.fetchone()

        if record:
            # SQL-запрос для обновления колонки record_check
            update_query = "UPDATE reports SET record_check = ? WHERE id_number = ?"
            cursor.execute(update_query, ("bad", record_id))
            conn.commit()
            greeting_post = (f"Записи с ID {record_id} помечена как 'bad'.\n\n\n"
                             "<b>Для возврата 🔙 в начало нажмите</b> /start")
            await message.answer(greeting_post)
        else:
            del_post = ("Записи с указанным ID не существует. Пожалуйста, введите корректный ID.\n\n\n"
                        "<b>Для возврата 🔙 в начало нажмите</b> /start")
            await message.answer(del_post)

        conn.close()
    except ValueError:
        greeting_post_error = ("Некорректный ID. Введите число.\n\n\n"
                               "<b>Для возврата 🔙 в начало нажмите</b> /start")
        await message.answer(greeting_post_error)
    finally:
        await state.finish()


def adjustment_registry_handler():
    """Регистрируем обработчики для корректировки"""
    dp.register_callback_query_handler(adjustment_record_handler)
    dp.register_callback_query_handler(adjustment_record_for_tomorrow_handler)
