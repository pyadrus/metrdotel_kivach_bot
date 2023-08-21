from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def greeting_keyboard():
    """Клавиатура админа"""
    greeting_key = InlineKeyboardMarkup()
    report_for_today_button = InlineKeyboardButton(text='✅ отчет ЗА СЕГОДНЯ', callback_data='report_for_today')
    report_for_tomorrow_button = InlineKeyboardButton(text='✅ отчет НА ЗАВТРА', callback_data='report_for_tomorrow')
    greeting_key.row(report_for_tomorrow_button, report_for_today_button)
    apply_button = InlineKeyboardButton(text='✅ Подать заявку', callback_data='apply')
    greeting_key.row(apply_button)
    correction_of_reports_key = InlineKeyboardButton(text="🛠 Корректировка отчетов", callback_data='correction_of_reports_key')
    greeting_key.row(correction_of_reports_key)

    return greeting_key


if __name__ == '__main__':
    greeting_keyboard()
