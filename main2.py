import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError
import Tokken
from re import findall

V = Tokken.V
token = Tokken.token
token_user = Tokken.token_user
vk = vk_api.VkApi(token=token)
vk_user = vk_api.VkApi(token=token_user)
longpoll = VkLongPoll(vk)
url_vk_id = 'https://vk.com/id'


class serch_users:
    def __init__(self, sex, city, age_from, age_to):
        self.sex = sex
        self.city = city
        self.age_from = age_from
        self.age_to = age_to

        self.list_of_peoples = []
        self.vk_user = vk_api.VkApi(token=token_user)

    def user(self):
        serch_parameters = self.vk_user.method('users.search',  # Параметры поиска
                                          {'sort': 0
                                              , 'hometown': self.city
                                              , 'sex': self.sex
                                              , 'age_from': self.age_from
                                              , 'age_to': self.age_to
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
            self.list_of_peoples.append(people)
        return self.list_of_peoples


class serch_photo:
    def __init__(self, user_id):
        self.user_id = user_id
        self.photo = []
        self.vk_user = vk_api.VkApi(token=token_user)
        self.V = Tokken.V
        self.result = []

    def serch_and_sorted(self):
        try:
            resp = self.vk_user.method('photos.get',
                                  {
                                      'access_token': self.vk_user
                                      , 'v': self.V
                                      , 'owner_id': self.user_id
                                      , 'album_id': 'profile'
                                      , 'count': 100
                                      , 'extended': 1
                                      , 'photo_sizes': 1
                                  })
        except ApiError:
            return 'нет доступа к фото'

        for i in range(100):
            try:
                self.photo.append(
                    (resp['items'][i]['likes']['count'],
                     'photo' + str(resp['items'][i]['owner_id']) + '_' + str(resp['items'][i]['id'])))
            except IndexError:
                self.photo.append(['нет фото'])

        for element in self.photo:
            if element != ['нет фото'] and self.photo != 'нет доступа к фото':
                self.result.append(element)

        return sorted(self.result, key=lambda x: (x[0], x[1]), reverse=True)[: 3]


def write_msg(user_id, message, attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment
        ,'random_id': randrange(10 ** 7)})


def msg():
    params = []
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text.lower()
                params.append(message_text)
                return message_text

class getting_param:
    def __init__(self):
        self.name = str()
        self.surname = str()
        self.vk_httml = str()
        self.vk_id_users = []
        self.params_user = []

    def msg_1(self):
        params_ = []
        serch_user_1 = []

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text.lower()
                    user_id = event.user_id

                    if str(request) == "3":  # Активация бота
                        write_msg(user_id, "Введите пол 1 - ж, 2- м: ")
                        params_.append(msg())
                    else:
                        write_msg(user_id , f"Ошибка! Введите корректные данные!")

                    if len(params_) == 1:
                        write_msg(user_id , "Введиет город: ")
                        params_.append(msg())
                        write_msg(user_id , "Введите возраст от: ")
                    else:
                        write_msg(user_id , f"Ошибка! Введите корректные данные!")

                    if 18 >= int(request) <= 40:
                        params_.append(int(msg()))
                        write_msg(user_id , "Введите возраст до: ")
                    else:
                        write_msg(user_id , f"Ошибка! Введите корректные данные!")

                    if int(params_[2]) >= int(request) <= 40:
                        params_.append(int(msg()))
                    else:
                        write_msg(user_id , f"Ошибка! Введите корректные данные!")

                    users = serch_users(params_[0], params_[1], params_[2],
                                                  params_[3])

                    serch_user_1.append(users.user())

                    for i in serch_user_1:
                        for t in i:
                            self.name = t[0]
                            self.surname = t[1]
                            self.vk_httml = t[2]
                            self.vk_id_user = t[3]
                            self.vk_id_users.append(self. vk_id_user)
                            self.params_user.append({self.vk_id_user: [self.name, self.surname, self.vk_httml]})
                        return self.params_user


def get_photo_in_msg():
    users_id = getting_param().msg_1()
    params = []

    for i in users_id:
        for k, v in i.items():
            ser_ph = serch_photo(k)
            p = ser_ph.serch_and_sorted()
            if p != 'нет доступа к фото':
                for photo in p:
                    params.append({photo[1]: v})

    for i in params:
        for k, v in i.items():
            write_msg('как вот тут получить id ?',' f"{v[0]} {v[1]} {v[2]}"
                       , attachment=k)

while True:
    get_photo_in_msg()

