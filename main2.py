import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.exceptions import ApiError
import Tokken


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


class getting_param:
    def __init__(self, params):
        self.serch_user_1 = params
        self.name = str()
        self.surname = str()
        self.vk_httml = str()
        self.vk_id_users = []
        self.params_user = []

    def msg_1(self):
        for i in self.serch_user_1:
            for t in i:
                self.name = t[0]
                self.surname = t[1]
                self.vk_httml = t[2]
                self.vk_id_user = t[3]
                self.vk_id_users.append(self. vk_id_user)
                self.params_user.append({self.vk_id_user: [self.name, self.surname, self.vk_httml]})
            return self.params_user



