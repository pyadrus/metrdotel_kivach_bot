from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def adjustment_keyboard():
    """Клавиатура корректировка отчетов"""
    adjustment_key = InlineKeyboardMarkup()
    for_tomorrow_key = InlineKeyboardButton(text="🛠 Корректировка отчета НА ЗАВТРА", callback_data='for_tomorrow_key')
    adjustment_key.row(for_tomorrow_key)
    today_key = InlineKeyboardButton(text="🛠 Корректировка отчета ЗА СЕГОДНЯ", callback_data='today_key')
    adjustment_key.row(today_key)

    return adjustment_key


if __name__ == '__main__':
    adjustment_keyboard()
