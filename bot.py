import apiai
import json
import vk_api
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
vk = vk_api.VkApi(token='779452e3cff26a88f0f7c693a31b22f91969e9d0578274af5476c1f64fc21636d23f70db3a9e1776a53a5', )

values = {'out': 0, 'count': 100, 'time_offset': 60}

response = vk.method('messages.get', values)

morph = pymorphy2.MorphAnalyzer()

import pymorphy2

# probability score threshold
prob_thresh = 0.4

morph = pymorphy2.MorphAnalyzer()

text = """
0989189960. Привет вам от Светланы.
А я из Мюнхена, звать меня Макс.
Андрея не забудьте. Нуууу как бы Олег.
Даниіл. Вітання від Даниіла.
"""


def write_message(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


def main():
    while True:
        vk = vk_api.VkApi(token='779452e3cff26a88f0f7c693a31b22f91969e9d0578274af5476c1f64fc21636d23f70db3a9e1776a53a5', )
        response = vk.method('messages.get', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['id']
        for item in response['items']:
            message = response['items'][0]['body']
            if not message:
                message = 'привет'
            request = apiai.ApiAI('17e75aa35a4a4bfa8a62d83fd3b825a3').text_request()  # Токен API к Dialogflow
            request.lang = 'ru'  # На каком языке будет послан запрос
            request.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
            request.query = message  # Посылаем запрос к ИИ с сообщением от юзера
            response_json = json.loads(request.getresponse().read().decode('utf-8'))

            response_bot = response_json['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
            # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял

            if response_bot:
                write_message(item['user_id'],
                              response_bot)
            else:
                write_message(item['user_id'],
                              'Я вас не совсем понял')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
