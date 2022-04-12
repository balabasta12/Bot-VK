from main2 import *
from random import randrange
from vk_api.longpoll import VkEventType


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


def main():
    serch_user_1 = []
    params_ = []
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()
                user_id = event.user_id
                write_msg(user_id, "Hey!!!")
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

                users_id = getting_param(serch_user_1).msg_1()
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
                        write_msg(user_id, f"{v[0]} {v[1]} {v[2]}"
                                   , attachment=k)

while True:
    main()
