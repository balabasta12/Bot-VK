from random import randrange
import Tokken
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = Tokken.token
token_user = Tokken.token_user

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

# Поиск людей
def serch_users(sex, city, age_from, age_to):
    list_of_peoples = []
    url_vk_id = 'https://vk.com/id'
    serch_parameters = vk.method('users.search',  # Параметры поиска
                         {
                             'sort': 1
                             ,'city': city
                             ,'sex': sex
                             ,'age_from': age_from
                             ,'age_to': age_to
                             ,'status': 1
                             ,'has_photo': 1
                             ,'count': 20
                         })

    for element in serch_parameters['items']:
        people = [
            element['first name']
            ,element['last_name']
            ,url_vk_id + str(element['id'])
            ,element['id']
        ]
        list_of_peoples.append(people)

    return list_of_peoples



for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()
            user_id = event.user_id

            if request == "привет":
                write_msg(user_id, f"Хай, {user_id}")
            elif request == "пока":
                write_msg(user_id, "Пока((")

            else:
                write_msg(user_id, "Не поняла вашего ответа...")


