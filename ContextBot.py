import requests
import telebot
import time
import ast
import re
import random

# Additional functions
def prepare_and_change_to_json(text):
    """Change string to correct form and transform to dict"""
    text = text.replace('false', 'False')
    text = text.replace('true', 'True')
    result = ast.literal_eval(text)
    return result

# Necessary constants
bot = telebot.TeleBot('API of the bot')
URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
URL_ANSWER = 'https://developers.lingvolive.com/api/v1/WordList'
KEY = 'Key for geting the Api'

# BASED_PARAMS = {'scrLang': 1033, 'dstLang'}
# database = []

# Request for api
headers_auth = {'Authorization': 'Basic ' + KEY}
auth = requests.post(URL_AUTH, headers=headers_auth)
API = auth.text
headers_answ = {'Authorization': 'Bearer ' + API}

# parameters for searching
# The appointment

@bot.message_handler(commands=['start'])
def start_mes(message):
    bot.send_message(message.chat.id,
                     "Hi, nice to meet you!")
    time.sleep(2)

    bot.send_message(message.chat.id,
                     'You should send me one word now.')


@bot.message_handler(content_types=['text'] )
def list_context_words(message):
    parameters = {'prefix': message.text,
                  'srcLang': 1033,
                  'dstLang': 1049,
                  'pageSize': 1000}
    try:
        answer = requests.get(URL_ANSWER, params=parameters, headers=headers_answ)
        result = prepare_and_change_to_json(answer.text).get('Headings')
        box = []
        count = 0
        i = random.randint(0, len(result) - 1)
        number_of_values = 6
        for _ in range(number_of_values):
            # while : Get rid of the repeated indexes and incorrect translation
            while i in box or re.search('[a-zA-Z]', result[i].get('Translation')):
                i = random.randint(0, len(result) - 1)
                count += 1
                if count > 100:
                    return
            box.append(i)
            bot.send_message(message.chat.id, result[i].get('Heading') + ' — ' + result[i].get('Translation'))

    except AttributeError:
        bot.send_message(message.chat.id, "Can't find this word, try another one!")


if __name__ == "__main__":
    try:
        bot.polling(non_stop=True)
    except requests.exceptions.InvalidHeader as e:
        print("One of the URLs is incorrect")
    except requests.exceptions.ConnectionError:
        print("Weak connection")
    except (SystemError, KeyboardInterrupt):
        print("The bot is taken off")
