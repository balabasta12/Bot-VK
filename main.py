from random import randrange
import Tokken
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

token = Tokken.token
token_user = Tokken.token_user
#
vk = vk_api.VkApi(token=token)
# vk = vk_api.VkApi(token=token_user)
longpoll = VkLongPoll(vk)


#  Кнопки
# keyboard = VkKeyboard(one_time=True)
# keyboard.add_button("Ведите пол", color=VkKeyboardColor.POSITIVE)
# keyboard.add_button("Введиет город: ", color=VkKeyboardColor.POSITIVE)
# keyboard.add_button("Введите возраст от: ", color=VkKeyboardColor.POSITIVE)
# keyboard.add_button("Введите возраст до: ", color=VkKeyboardColor.POSITIVE)


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
            ,url_vk_id + str(element["id"])
            ,element['id']
        ]
        list_of_peoples.append(people)

    return list_of_peoples
# a = serch_users(2, 'Москва', 20, 21)
# print(a)

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
                                     ,'count': 5
                                     ,'extended': 1
                                 })
    except:  # На какую ошибку указывать?
        return 'Нет доступа к фото'

    for i in range(5):
        try:
            list_photo.append(
                [serch_photo['items'][i]['likes']['count'],
                 'photo' + str(serch_photo['items'][i]['owner_id']) + '_' + str(serch_photo['items'][i]['id'])])
        except IndexError:
            list_photo.append(['Нет фото'])
    return list_photo
# print(serch_photo())

def max_likes(user_photos):
    photo = []
    for element in user_photos:
        if element != 'Нет фото' and user_photos != 'Нет доступа к фото':
            photo.append(element)
    return sorted(photo)
# a = max_likes(serch_photo())
# print(a)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})  # 'keyboard': keyboard.get_keyboard()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()
            user_id = event.user_id

            if request == "привет":
                write_msg(user_id, f"Хай, {user_id}")
            elif request == "пока":
                write_msg(user_id, "Пока((")

            elif request == "1":
                gender = input("Введите пол 1 - ж, 2- м: ")
                city = input("Введиет город: ")
                age_from = input("Введите возраст от: ")
                age_to = input("Введите возраст до: ")
                serch_users = serch_users(gender, city, age_from, age_to)
                for i in serch_users:
                    write_msg(user_id, f"{i}\n")

            else:
                write_msg(user_id, "Не поняла вашего ответа...")