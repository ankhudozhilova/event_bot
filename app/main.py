import telebot
import pyqrcode
from io import BytesIO
import event_bot.dbutils.utils as utils
import event_bot.dbutils.dbconfig as config
from event_bot.data.Events import Event


TOKEN = "1915200271:AAGSnwocGS-EgHPhPi57lJSZaKrE2pl05hk"
HELP = """
/help - помощь\n
/show - список мероприятий\n
/ticket - заказ билета на мероприятие\n
/events - Ваши мероприятия\n
"""
STATE_CMD = 0
STATE_EVENT_ID = 1
STATE_PLACES = 2

def find_event(eid, elist):
    event = Event()
    for e in elist:
        if eid == e.id:
            event.id = e.id
            event.event = e.event
            event.date = e.date
            event.time = e.time
            event.location = e.location
            event.places = e.places
            break
    return event

state = STATE_CMD
current_event = Event()
bot = telebot.TeleBot(TOKEN)
events = utils.get_events()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global state, events, current_event

    if state == STATE_CMD:
        if message.text == "/start":
            bot.send_message(message.from_user.id, 'Напишите мне "Привет"')
        elif message.text == "Привет":
            bot.send_message(message.from_user.id,
                             "Привет, я бот для записи на мароприятия. Для помощи наберите команду /help")
        elif message.text == "/help":
            bot.send_message(message.from_user.id, HELP)
        elif message.text == "/ticket":
            bot.send_message(message.from_user.id, "Введите номер мероприятия")
            state = STATE_EVENT_ID
        elif message.text == "/show":
            msg = ""
            for e in events:
                msg += e.to_string() + "\n"
            bot.send_message(message.from_user.id, msg)
        elif message.text == "/events":
            events = utils.get_events_by_user(message.from_user.id)
            if len(events) > 0:
                msg = ""
                for event in events:
                    msg += event + "\n"
                bot.send_message(message.from_user.id, msg)
            else:
                bot.send_message(message.from_user.id, "Вы не регистрировались на наши мероприятия. Для заказа билате "
                                                       "выполните команду /ticket")
    elif state == STATE_EVENT_ID:
        if message.text.isdigit():
            eid = int(message.text)
            current_event = find_event(eid, events)
            if current_event.id < 0:
                bot.send_message(message.from_user.id, "Такого мероприятия нет")
                state = STATE_CMD
            else:
                bot.send_message(message.from_user.id, "Введите количество мест")
                state = STATE_PLACES
        else:
            bot.send_message(message.from_user.id, "Введите номер мероприятия")
    elif state == STATE_PLACES:
        if message.text.isdigit():
            amount = int(message.text)
            eid, amount, ticket = utils.create_ticket(current_event.id, message.from_user.id, amount)
            if ticket == config.NO_TICKETS:
                bot.send_message(message.from_user.id, "Такого количества мест нет")
            else:
                events = utils.get_events()
                data = "EventID=" + str(eid) + " " + str(amount) + " places" #"#ticket.encode()
                image = pyqrcode.create(data)
                buffer = BytesIO()
                image.png(buffer, scale=10)
                bot.send_photo(message.from_user.id, photo=buffer.getvalue())
                state = STATE_CMD
        else:
            bot.send_message(message.from_user.id, "Введите количество мест")


bot.polling(none_stop=True, interval=0)
