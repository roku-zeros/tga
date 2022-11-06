from django.core.management.base import BaseCommand
from django.conf import settings

from telebot import TeleBot
from pyqiwip2p import QiwiP2P

from utils.choices import *
from utils.markups import *
from utils.states import *
from ugc.models import *


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)
key = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Im9rMHFjNC0wMCIsInVzZXJfaWQiOiI3OTE2MjY4NzkxMSIsInNlY3JldCI6ImU5MzU0YzQxZmFhMGMwOTY3NWY3MzBiMTgwYjUxOGFjMDMyYTI0NGEyZDg1OGY5MzY2Nzc0OTc1YjhiMTgzODAifX0="
p2p = QiwiP2P(auth_key=key)


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()


@bot.message_handler(commands=['start'])
def start_message(message):
    profile, created = Profile.objects.get_or_create(external_id=message.chat.id, name=message.from_user.username)

    msg = bot.send_message(profile.external_id, 'Привет, тут ты можешь купить тесты.').id
    bot.send_message(profile.external_id, 'Выбери год', reply_markup=years_markup())

    profile.state = 1
    profile.order_msg_id = msg
    profile.order_msg = ""
    profile.save()


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = Profile.objects.get(external_id=call.from_user.id, name=call.from_user.username)
    print(call.data)
    # Get user from call and his state
    user_state = user.state

    if call.data == "back":
        user.go_back()

    if user_state == YEAR_SELECTION_STATE:
        bot.send_message(call.from_user.id, 'Выбери год', reply_markup=years_markup())
        user.go_next()

    elif user_state == MONTH_SELECTION_STATE:
        user.order_msg += f"Год: {call.data}\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выбери месяц',
                              reply_markup=month_markup())
        user.go_next()

    elif user_state == COUNTRY_SELECTION_STATE:
        user.order_msg += f"Месяц: {call.data}\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выбери страну',
                              reply_markup=countries_markup())
        # bot.send_message(user, 'Выбери страну', reply_markup=countries_markup())
        user.go_next()
    elif user_state == DIRECTION_SELECTION_STATE:
        user.order_msg += f"Страна: {call.data}\n"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выбери направление',
                              reply_markup=direction_markup())
        # bot.send_message(user, 'Выбери направление', reply_markup=direction_markup())
        user.go_next()
    elif user_state == BD_SELECTION_STATE:
        user.order_msg += f"Направление: {call.data}\n"
        order = user.get_order()
        choices = Product.objects.filter(year=order[0], country=order[2], direction=order[3])[0:5]

        keyboard = telebot.types.InlineKeyboardMarkup()
        for i in range(len(choices)):
            key = telebot.types.InlineKeyboardButton(text=f"Тест #{order.id}", callback_data=order.id)
            keyboard.add(key)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выбери тест',
                              reply_markup=keyboard)
        user.go_next()
    elif user_state == PAYMENT_STATE:
        comment = "Тестовая оплата для бота)"
        bill = p2p.bill(amount=1, lifetime=10, comment=comment)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Произведите оплату по ссылке\n{bill.pay_url}")
        # bot.send_message(user, f"Произведите оплату по ссылке\n{bill.pay_url}")
        pass
    else:  # Something went bad
        print("bad state")

    user.save()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=user.order_msg_id,
                          text=user.order_msg)


def run_bot():
    bot.polling(none_stop=True, interval=0)