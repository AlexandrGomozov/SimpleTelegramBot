import random
import telebot
import pickle

ver = "2.0.0"

developments = """====МАШТАБНОЕ ОБНОВЛЕНИЕ {}====
- исправлено 5 багагов

- добавлены задачи (помочь маме,сходить в школу)
 
- переделаны команды (show_all, show,done,reset)

- теперь есть разделение по пользователям

- добавлены комады (add_wishes, good, bad, start) 
""".format(ver)

RANDOM_BAY = ["До свидания!", "скоро увидимся!", "до новых встреч!", "приятно было иметь дело с вами! ;)"]

RANDOM_HELLO = ["привет от старых штеблет ;)", "привет :)", "hello", "здравствуйте!!!"]

RANDOM_TASK = ["cделать уроки", "убраться", "помыть машину", "написать письмо деду морозу", "купить горошек",
               "покормить кота", "помыть улиток", "погулять", "починить лампу", "выучить питон", "помочь маме",
               "сходить в школу"]

RANDOM_GOOD = ["спасибо за оценку!", "рад что вы оценили :)", "я тоже так думаю ;)"]

RANDOM_BAD = ["спасибо за оценку!", "рад что вы оценили :(", "а почему сразу плохо?", "я иправлю все недостатки!"]


HELP = """

/help - напечатать справку по коммандам

/start - напечатать справку по боту

/bay - вывести прощание

/hello - вывести приветствие

/good, bad - вывести ответ на оценку  

/ver  - напечатать версию программы

/add  - добавить задачу в список (дата) (задача)

/add_random - добавить случайную задачу на сегодня

/show - напечатать задачи на определённую дату (дата)

/show_all - напечатать все задачи

/development - вывести информацию о событиях и обновлениях

/reset - очистить список задач

/done - отметить задачу выполненой (дата) (задача)

/add_wishes - пожелание на следуюшею версию (пожелание)
"""

tasks = {}
try:
    file = open('token.txt', 'r')
    token = file.readline()
except Exception as a:
    print("Can't open token.txt file")
finally:
    file.close()

bot = telebot.TeleBot(token)

class Task:
    def __init__(self, text):
        self.text = text
        self.done = False


try:
    file = open('telegram.pkl', 'rb')
    tasks = pickle.load(file)
except FileNotFoundError:
    file = open('telegram.pkl', 'wb')
    tasks = {}
finally:
    file.close()


def add_task(date, text, id):
    if id in tasks:
        if date in tasks[id]:
            tasks[id][date].append(Task(text))
        else:
            tasks[id][date] = [Task(text)]
    else:
        tasks[id] = {date: [Task(text)]}
    save_tasks()


def save_tasks():
    file = open('telegram.pkl', 'wb')
    try:
        pickle.dump(tasks, file)
    finally:
        file.close()


def show_day_tasks(date, id):
    text = "=====" + date + "=====\n"
    for t in tasks[id][date]:
        if t.done == False:
            text = text + '- ' + str(t.text) + "\n"
        else:
            text = text + '+ ' + str(t.text) + "\n"
    return text


@bot.message_handler(commands=['start'])
def show_ver(message):
    bot.send_message(message.chat.id, "добро пожаловать в Todo бота, его версия ", ver, ", чтобы получить более подробную информация о командах можно задав команду help")


@bot.message_handler(commands=['reset'])
def reset(message):
    tasks[message.from_user.id] = {}
    save_tasks()
    bot.send_message(message.chat.id, "Список задач очищен!")


@bot.message_handler(commands=['development'])
def show_development(message):
    bot.send_message(message.chat.id, developments)


@bot.message_handler(commands=['help', '?'])
def show_help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['hello'])
def show_hello(message):
    bot.send_message(message.chat.id, random.choice(RANDOM_HELLO))


@bot.message_handler(commands=['bay'])
def show_bay(message):
    bot.send_message(message.chat.id, random.choice(RANDOM_BAY))


@bot.message_handler(commands=['done'])
def done(message):
    splitted_message = message.text.split(maxsplit=2)
    if len(splitted_message) == 3:
        date = splitted_message[1].lower()
        text = splitted_message[2].lower()
        id = message.from_user.id
        if id in tasks:
            if date in tasks[id]:
                for t in tasks[id][date]:
                    if t.text == text:
                        t.done = True
                        bot.send_message(message.chat.id, "Задача: " + text + " выполнена")
        else:
            bot.send_message(message.chat.id, "У вас нет задач")
    else:
        bot.send_message(message.chat.id, "Неверный формат команды %(")
    save_tasks()


@bot.message_handler(commands=['ver'])
def show_ver(message):
    bot.send_message(message.chat.id, ver)


@bot.message_handler(commands=['good'])
def show_class(message):
    bot.send_message(message.chat.id, random.choice(RANDOM_GOOD))


@bot.message_handler(commands=['bad'])
def show_bad(message):
    bot.send_message(message.chat.id, random.choice(RANDOM_BAD))


@bot.message_handler(commands=['add_wishes'])
def add_wish(message):
    splitted_message = message.text.split(maxsplit=1)
    if len(splitted_message) == 2:
        str1 = u"Пожелание: " + splitted_message[1] + u" от: " + str(message.from_user.first_name) + u"\n"
        try:
            file = open('wishes.txt', 'a+')
            file.write(str1)
        finally:
            file.close()
        bot.send_message(message.chat.id, "Ваше пожелание возможно будет реализовоно")
    else:
        bot.send_message(message.chat.id, "Неправильный формат команды %(")


@bot.message_handler(commands=['add'])
def add(message):
    try:
        splitted_message = message.text.split(maxsplit=2)
        date = splitted_message[1].lower()
        text = splitted_message[2].lower()
        add_task(date, text, message.from_user.id)
        bot.send_message(message.chat.id, "Задача: " + str(text) + " добавлена, на дату: " + str(date))
    except Exception as a:
        bot.reply_to(message, str(a))


@bot.message_handler(commands=['add_random'])
def add_random_task(message):
    date = "Cегодня"
    text = random.choice(RANDOM_TASK)
    add_task(date, text, message.from_user.id)
    bot.send_message(message.chat.id, "Задача: " + text + " добавлена на дату:" + date)


@bot.message_handler(commands=['show', 'print'])
def show(message):
    id = message.from_user.id
    try:
        splitted_message = message.text.split(maxsplit=1)
        if len(splitted_message) == 2:
            date = splitted_message[1]
            if date in tasks[id]:
                text = show_day_tasks(date, id)
                bot.send_message(message.chat.id, text)
            else:
                bot.send_message(message.chat.id, "Такой даты нет :(")
        else:
            bot.send_message(message.chat.id, "Такой даты нет :(")
    except Exception as a:
        bot.reply_to(message, str(a))


@bot.message_handler(commands=['show_all'])
def show_all(message):
    id = message.from_user.id
    try:
        text = ""
        for key in tasks[id]:
            text = text + show_day_tasks(key, id)
        if text == "":
            bot.send_message(message.chat.id, "Список задач пуст :(")
        else:
            bot.send_message(message.chat.id, text)
    except Exception as a:
        bot.reply_to(message, str(a))


@bot.message_handler(content_types=["text"])
def show_error(message):
    bot.send_message(message.chat.id, "Команда не известна :( ")


bot.polling(none_stop=True)
