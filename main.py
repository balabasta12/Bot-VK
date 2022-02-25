from random import randrange
import Tokken
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


token = Tokken.token
token_user = Tokken.token_user
vk = vk_api.VkApi(token=token)
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
                                      {     'sort': 0
                                          , 'hometown': city
                                          , 'sex': sex
                                          , 'age_from': age_from
                                          , 'age_to': age_to
                                          , 'status': 6
                                          , 'count': 5
                                          , 'has_photo': 1
                                      })

    for element in serch_parameters['items']:
        people = [
            element['first_name']
            , element['last_name']
            , url_vk_id + str(element["id"])
            , element['id']
        ]
        list_of_peoples.append(people)

    return list_of_peoples


# Поиск фото
def serch_photo(user_id):
    vk_user = vk_api.VkApi(token=token_user)

    try:
        resp = vk_user.method('photos.get',
                                     {
                                         'access_token': vk_user
                                         , 'v': token
                                         , 'owner_id': user_id
                                         , 'album_id': 'profile'
                                         , 'count': 5
                                         , 'extended': 1
                                         , 'photo_sizes': 1


                                     })
    except ApiError:  # На какую ошибку указывать?
        return 'Нет доступа к фото'

    serch_photo = []

    for i in range(5):
        try:
            serch_photo.append(
                [resp['items'][i]['likes']['count'],
                 'photo' + str(resp['items'][i]['owner_id']) + '_' + str(resp['items'][i]['id'])])
        except IndexError:
            serch_photo.append(['Нет фото'])
    return serch_photo


def sort_likes(user_photos):
    photo = []
    for element in user_photos:
        if str(element) != 'Нет фото' and str(user_photos) != 'Нет доступа к фото':
            photo.append(element)
    return sorted(photo)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,
                                'random_id': randrange(10 ** 7)})  # 'keyboard': keyboard.get_keyboard()


def msg():
    params = []
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text.lower()
                params.append(message_text)
                return message_text


for event in longpoll.listen():
    params_ = []
    id_users = []
    sort_ = []


    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()
            user_id = event.user_id

            if str(request) == "3":
                write_msg(user_id, "Введите пол 1 - ж, 2- м: ")
                params_.append(msg())

            if len(params_) == 1:
                write_msg(user_id, "Введиет город: ")
                params_.append(msg())
                write_msg(user_id, "Введите возраст от: ")

            if 18 >= int(request) <= 40:
                params_.append(int(msg()))
                write_msg(user_id, "Введите возраст до: ")

            if int(params_[2]) >= int(request) <= 40:
                params_.append(int(msg()))

            else:
                write_msg(user_id, f"Ошибка! Введите корректные данные!")

            serch_users = serch_users(params_[0], params_[1], params_[2], params_[3])  # Получаем параметры для поиска людей


            for i in serch_users:
                # write_msg(user_id, f"{i[0]} {i[1]} {i[2]}\n")
                id_users.append(f"{i[3]}")



            for photo in id_users:
                photo_ = serch_photo(photo)
                a = {photo: photo_}
                for values in a.values():
                    # b = sort_likes(values)
                    for i in values:
                        b = sort_likes(i)







