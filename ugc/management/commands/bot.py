from django.core.management.base import BaseCommand
from django.conf import settings

from telebot import TeleBot
from pyqiwip2p import QiwiP2P
from coinbase_commerce.client import Client
from io import BytesIO

from utils.choices import *
from utils.markups import *
from utils.states import *
from ugc.models import *
from utils.checks import qiwi_check, crypto_check

# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)
API_KEY = "a2b45d1c-5cb8-4342-a287-ee7022fbef99"
client = Client(api_key=API_KEY)
QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjZyMXcyZC0wMCIsInVzZXJfaWQiOiI3OTc3MTI2NTAzOSIsInNlY3JldCI6ImRhNDE3NzUyNjI5MzMwZTU5ZDY0MmRhZDcwNzc4OTJlZDNkYjU4ZWQ4YTE0MTAyZmY3ZWI2YzY1NjA1NzQ1YTcifX0="
p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)


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


@bot.message_handler(commands=['buy'])
def start_message(message):
    profile, created = Profile.objects.get_or_create(external_id=message.chat.id, name=message.from_user.username)

    msg = bot.send_message(profile.external_id, '_____.').id
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
    elif call.data == 'get_file':
        payment = user.payment_id.split('#')
        product = Product.objects.get(id=user.basket)
        if payment[0] == 'qiwi':
            status = 12 #p2p.check(bill_id=payment[1]).status
            print(product.file)
            if status != 'PAID':
                bot.send_document(call.from_user.id, document=product.file, caption='Тест')
                bot.send_message(user.external_id, 'Чтобы купить еще один тетст нажми: /buy')
            else:
                bot.send_message(call.from_user.id, 'Оплата еще не прошла')
        else:
            retrieved_charge = client.charge.retrieve(entity_id=payment[1])
            status = retrieved_charge['timeline'][-1]['status']
            if status in ['Completed', 'Resolved']:
                bot.send_document(call.from_user.id, document=product.file, caption='Тест')
                bot.send_message(user.external_id, 'Чтобы купить еще один тетст нажми: /buy')
            else:
                bot.send_message(call.from_user.id, 'Оплата еще не прошла')



    elif call.data == 'qiwi' or call.data == 'crypto':
        product = Product.objects.get(id=user.basket)
        check_id = ""
        url = ""
        if call.data == 'qiwi':
            check_id, url = qiwi_check(product)
            user.payment_id = f"qiwi#{url}"
        else:
            check_id, url = crypto_check(product)
            user.payment_id = f"crypto#{url}"
        print("QIWI ID ", check_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Произведи оплату по ссылке и нажмите на кнопку:\n{url}",
                              reply_markup=check_markup())

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
            key = telebot.types.InlineKeyboardButton(text=f"Тест #{choices[i].id}", callback_data=choices[i].id)
            keyboard.add(key)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выбери тест',
                              reply_markup=keyboard)
        user.go_next()
    elif user_state == PAYMENT_STATE:
        user.order_msg += f"\nТест #{call.data}\n"
        user.basket = call.data

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выбери способ оплаты',
                              reply_markup=payment_markup())
        user.go_next()
    elif user_state == FINAL_STATE:
        return
    else:  # Something went bad
        print("bad state")

    user.save()
    print(user_state)
    if 1 <= user_state <= 4:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=user.order_msg_id,
                              text=user.order_msg)


def run_bot():
    bot.polling(none_stop=True, interval=0)
