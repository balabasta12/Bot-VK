import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError
import Tokken

V = Tokken.V
token = Tokken.token
token_user = Tokken.token_user
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)



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
                                          , 'online': 1
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
                                         , 'v': V
                                         , 'owner_id': user_id
                                         , 'album_id': 'profile'
                                         , 'count': 5
                                         , 'extended': 1
                                         , 'photo_sizes': 1


                                     })
    except ApiError:
        return 'нет доступа к фото'

    serch_photo = []
    not_f = []
    for i in range(5):
        try:
            serch_photo.append(
                {resp['items'][i]['likes']['count']:
                 'photo' + str(resp['items'][i]['owner_id']) + '_' + str(resp['items'][i]['id'])})
        except IndexError:
            serch_photo.append(['нет фото'])
    return serch_photo


def sort_likes(photos):
    result = []
    res = []
    for element in photos:
        if element != ['нет фото'] and photos != 'нет доступа к фото':
            result.append(element)
    for i in result:
        sorted_tuple = sorted(i .items(), key=lambda x: x[0])
        res.append(dict(sorted_tuple))
    return res




def write_msg(user_id, message, attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message,
                                'random_id': randrange(10 ** 7), 'attachment': attachment})  # 'keyboard': keyboard.get_keyboard()


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
    name_ = []


    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()
            user_id = event.user_id


            if str(request) == "3":
                write_msg(user_id, "Введите пол 1 - ж, 2- м: ")
                params_.append(msg())
            else:
                write_msg(user_id, f"Ошибка! Введите корректные данные!")

            if len(params_) == 1:
                write_msg(user_id, "Введиет город: ")
                params_.append(msg())
                write_msg(user_id, "Введите возраст от: ")
            else:
                write_msg(user_id, f"Ошибка! Введите корректные данные!")

            if 18 >= int(request) <= 40:
                params_.append(int(msg()))
                write_msg(user_id, "Введите возраст до: ")
            else:
                write_msg(user_id, f"Ошибка! Введите корректные данные!")

            if int(params_[2]) >= int(request) <= 40:
                params_.append(int(msg()))

            else:
                write_msg(user_id, f"Ошибка! Введите корректные данные!")

            serch_users = serch_users(params_[0], params_[1], params_[2], params_[3])  # Получаем параметры для поиска людей


            for i in serch_users:
                # write_msg(user_id, f"{i[0]} {i[1]} {i[2]}\n")
                name_.append(f"{i[0]} {i[1]} {i[2]}")
                id_users.append(f"{i[3]}")

            for id_user in id_users:
                sort_like = sort_likes(serch_photo(id_user))
                for sort_l in sort_like:
                    for photo in sort_l.values():
                        write_msg(user_id, f"Фото:", attachment=photo) # Как добавить мена к фото?






