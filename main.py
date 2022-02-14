from random import randrange
import Tokken
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = Tokken.token
token_user = Tokken.token_user
#
# vk = vk_api.VkApi(token=token)
vk = vk_api.VkApi(token=token_user)
longpoll = VkLongPoll(vk)

#
# def write_msg(user_id, message):
#     vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

# Поиск людей
def serch_users(sex, city, age_from, age_to):
    list_of_peoples = []
    url_vk_id = 'https://vk.com/id'
    vk_user = vk_api.VkApi(token=token_user)
    serch_parameters = vk_user.method('users.search',  # Параметры поиска
                         {
                             'sort': 1
                             ,'hometown': city
                             ,'sex': sex
                             ,'age_from': age_from
                             ,'age_to': age_to
                             ,'status': 1
                             ,'count': 20

                         })

    for element in serch_parameters['items']:
        people = [
            element['first_name']
            ,element['last_name']
            ,url_vk_id + str(element['id'])
            ,element['id']
        ]
        list_of_peoples.append(people)
    return list_of_peoples
# a = serch_users(2, 'Москва', 20, 21)
# b = []
# for i in a:
#     b.append(i[3])
#
# print(b)


# Поиск фото
def serch_photo(user_id):
    list_photo = []
    vk_user = vk_api.VkApi(token=token_user)

    try:
        serch_photo = vk_user.method('photos.get',
                                 {
                                     'access_token': vk_user
                                     ,'owner_id': user_id
                                     ,'album_id': 'profile'
                                     ,'count': 3
                                     ,'extended': 1
                                 })
    except:  # На какую ошибку указывать?
        return 'Нет доступа к фото'

    for i in range(3):
        try:
            list_photo.append(
                [serch_photo['items'][i]['likes']['count'],
                 'photo' + str(serch_photo['items'][i]['owner_id']) + '_' + str(serch_photo['items'][i]['id'])])
        except IndexError:
            list_photo.append(['Нет фото'])
    return list_photo
#print(serch_photo(701979327))



# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#
#         if event.to_me:
#             request = event.text.lower()
#             user_id = event.user_id
#
#             if request == "привет":
#                 write_msg(user_id, f"Хай, {user_id}")
#             elif request == "пока":
#                 write_msg(user_id, "Пока((")
#
#             else:
#                 write_msg(user_id, "Не поняла вашего ответа...")
