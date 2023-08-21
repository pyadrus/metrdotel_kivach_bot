from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.user_keyboards import greeting_keyboard
from messages.greeting_post import greeting_post
from system.dispatcher import dp


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия"""
    await state.finish()
    await state.reset_state()
    greeting_key = greeting_keyboard()
    # Клавиатура для Калькулятора цен или Контактов
    await message.reply(greeting_post, reply_markup=greeting_key, disable_web_page_preview=True,
                        parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def handle_unknown_message(message: types.Message):
    """Обработчик неизвестных сообщений"""
    await message.reply("Извините, я не понимаю ваш запрос. Пожалуйста, используйте меню ниже:",
                        reply_markup=greeting_keyboard(),
                        parse_mode=types.ParseMode.HTML)


def adding_track_number_handler():
    """Регистрируем handlers для обработчиков сообщений"""
    dp.register_message_handler(greeting)
    dp.register_message_handler(handle_unknown_message)

