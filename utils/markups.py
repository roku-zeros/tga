import telebot
from emoji import emojize
from utils.choices import DIRECTION_CHOICES, MONTH_CHOICES


def years_markup():
    keyboard = telebot.types.InlineKeyboardMarkup()
    key1 = telebot.types.InlineKeyboardButton(text=f"2017", callback_data="2017")
    key2 = telebot.types.InlineKeyboardButton(text=f"2018", callback_data="2018")
    keyboard.row(key1, key2)
    key1 = telebot.types.InlineKeyboardButton(text=f"2019", callback_data="2019")
    key2 = telebot.types.InlineKeyboardButton(text=f"2020", callback_data="2020")
    keyboard.row(key1, key2)
    key1 = telebot.types.InlineKeyboardButton(text=f"2021", callback_data="2021")
    key2 = telebot.types.InlineKeyboardButton(text=f"2022", callback_data="2022")
    keyboard.row(key1, key2)

    # Add button for going back
    key_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="back")
    # keyboard.add(key_back)
    return keyboard


def month_markup():
    keyboard = telebot.types.InlineKeyboardMarkup()

    for i in range(0, len(MONTH_CHOICES), 3):
        key1 = telebot.types.InlineKeyboardButton(text=str(MONTH_CHOICES[i][0]),
                                                  callback_data=str(MONTH_CHOICES[i][0]))
        key2 = telebot.types.InlineKeyboardButton(text=str(MONTH_CHOICES[i + 1][0]),
                                                  callback_data=str(MONTH_CHOICES[i + 1][0]))
        key3 = telebot.types.InlineKeyboardButton(text=str(MONTH_CHOICES[i + 2][0]),
                                                  callback_data=str(MONTH_CHOICES[i + 2][0]))
        keyboard.row(key1, key2, key3)

    # Add button for going back
    key_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="back")
    # keyboard.add(key_back)

    return keyboard


def countries_markup():
    keyboard = telebot.types.InlineKeyboardMarkup()

    key1 = telebot.types.InlineKeyboardButton(text=f"Россия {emojize(':Russia:')}", callback_data="Россия")
    key2 = telebot.types.InlineKeyboardButton(text=f"Казахстан {emojize(':Kazakhstan:')}", callback_data="Казахстан")
    keyboard.row(key1, key2)
    key1 = telebot.types.InlineKeyboardButton(text=f"Беларусь {emojize(':Belarus:')}", callback_data="Беларусь")
    key2 = telebot.types.InlineKeyboardButton(text=f"Украина {emojize(':Ukraine:')}", callback_data="Украина")
    keyboard.row(key1, key2)
    # Add button for going back
    key_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="back")
    # keyboard.add(key_back)
    return keyboard


def direction_markup():
    keyboard = telebot.types.InlineKeyboardMarkup()

    for i in range(0, len(DIRECTION_CHOICES), 2):
        key1 = telebot.types.InlineKeyboardButton(text=str(DIRECTION_CHOICES[i][0]),
                                                  callback_data=str(DIRECTION_CHOICES[i][0]))
        key2 = telebot.types.InlineKeyboardButton(text=str(DIRECTION_CHOICES[i + 1][0]),
                                                  callback_data=str(DIRECTION_CHOICES[i + 1][0]))
        keyboard.row(key1, key2)

    # Add button for going back
    key_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="back")
    # keyboard.add(key_back)

    return keyboard


def payment_markup():
    keyboard = telebot.types.InlineKeyboardMarkup()
    key1 = telebot.types.InlineKeyboardButton(text=f"Qiwi", callback_data="qiwi")
    key2 = telebot.types.InlineKeyboardButton(text=f"Криптовалюта", callback_data="crypto")
    keyboard.row(key1, key2)

    # Add button for going back
    key_back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="back")
    # keyboard.add(key_back)
    return keyboard
