import fake_useragent
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

from auth_data import token


def anekdot_one_line(anekdot_text):  # функция преобразовывает массив строк в одну строку
    anekdot_text_one_line = ""

    for str in anekdot_text:
        anekdot_text_one_line += str.text

    return anekdot_text_one_line


def get_anekdot(url):  # получения анекдотов со страницы

    user = fake_useragent.UserAgent().random  # получение фейкового user-agent

    headers = {
        "user-agent": user,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9 "
    }

    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    anekdots = soup.find_all("div", class_="anekdot")  # получаем все анекдоты со страницы

    all_anekdots_texts = []

    for anekdot in anekdots:  # проходимся по всем анекдотам для получения их текстов
        anekdot_text = anekdot.find_all("p")
        # print(anekdot_one_line(anekdot_text)) # преобразовываем массив строк в одну строку
        all_anekdots_texts.append(anekdot_one_line(anekdot_text))
    return all_anekdots_texts


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    types_and_urls = {
        "армия": "http://anekdotov.net/army/",
        "дети": "http://anekdotov.net/children/",
        "душевные": "http://anekdotov.net/story/simple/",
        "животные": "http://anekdotov.net/animals/",
        "женщины": "http://anekdotov.net/women/",
        "медицина": "http://anekdotov.net/story/med/",
        "компьютер": "http://anekdotov.net/computer/",
        "курьёзы": "http://anekdotov.net/bez/",
        "пикантные": "http://anekdotov.net/adult/",
        "розыгрыши": "http://anekdotov.net/prikol/",
        "реклама": "http://anekdotov.net/reklama/",
        "студенты": "http://anekdotov.net/students/",
        "пьяные": "http://anekdotov.net/trezv/",
        "транспорт": "http://anekdotov.net/transport/",
        "классика": "http://anekdotov.net/best/boroda/"
    }

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(
            message.chat.id,
            "Привет, выбери категорию анекдотов: \n Aрмия \n дети \n душевные \n животные \n женщины \n медицина \n "
            "компьютер \n курьёзы \n пикантные (16+) \n розыгрыши \n реклама \n студенты \n пьяные \n транспорт \n "
            "классика")

    @bot.message_handler(content_types=['text'])
    def show_anekdots(message):

        flag = False

        for key in types_and_urls:
            if key.lower() == message.text.lower():
                flag = True
                url = types_and_urls.get(key)

                anekdots = get_anekdot(url)

                for anekdot in anekdots:
                    bot.send_message(message.chat.id, anekdot)

        if flag == False:
            bot.send_message(message.chat.id, "Проверье корректность отправленной категории")
    bot.polling()


def main():
    # get_anekdot("https://anekdotov.net/")
    telegram_bot(token)


if __name__ == "__main__":
    main()
