#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
import requests
import vk_api
from colorama import Style, Fore
from python3_anticaptcha import ImageToTextTask
from vk_api.longpoll import VkEventType, VkLongPoll


class Base():

    def __init__(self):
        self.y = Fore.LIGHTYELLOW_EX  # ярко-жёлтый цвет
        self.g = Fore.LIGHTGREEN_EX  # ярко-зелёный цвет
        self.r = Fore.LIGHTRED_EX  # ярко-красный цвет
        self.d = Style.RESET_ALL  # очистка цветов
        self.plus = f'{self.g}[{self.d} + {self.g}]{self.d}'
        self.exclamation_point = f'{self.r}[{self.d} ! {self.r}]{self.d}'

    def intro(self):
        print('''              _                                            _           
             | |                                          | |          
   __ _ _   _| |_ ___  _ __ ___  ___ _ __   ___  _ __   __| | ___ _ __ 
  / _` | | | | __/ _ \| '__/ _ \/ __| '_ \ / _ \| '_ \ / _` |/ _ \ '__|
 | (_| | |_| | || (_) | | |  __/\__ \ |_) | (_) | | | | (_| |  __/ |   
  \__,_|\__,_|\__\___/|_|  \___||___/ .__/ \___/|_| |_|\__,_|\___|_|   
                                    | |                                
                                    |_|                                ''')
        self.greeting()

    def greeting(self):
        while True:
            try:
                print('Выберите способ авторизации:')
                self.authorization_method = int(input(f'\n{self.y}[{self.d}1{self.y}]{self.d} Через логин и пароль\n'
                                                      f'{self.y}[{self.d}2{self.y}]{self.d} Через токен\n'))
                if self.authorization_method == 1:
                    self.authorization_passlog()
                    break
                elif self.authorization_method == 2:
                    self.authorization_token()
                    break
                else:
                    print(f'\n{self.exclamation_point} Введите 1 или 2!')
            except:
                print(f'\n{self.exclamation_point} Введите цифру!')

    def authorization_passlog(self):
        while True:
            try:
                number = input(f'\n{self.plus} Введите номер: ')
                password = input(f'{self.plus} Введите пароль: ')
                url = f"https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqy" \
                      f"rnABp8ncuU&username={number}&password={password}"
                ke = requests.get(url).json()
                self.token = ke['access_token']
                vk = vk_api.VkApi(token=self.token)
                info_account = vk.method('users.get', {})
                fn = info_account[0]["first_name"]
                ln = info_account[0]["last_name"]
                print(f'\n{self.g}Аккаунт {fn} {ln} был успешно авторизован!{self.d}')
                self.authorization_token_anticaptcha()
                break
            except:
                print(f'\n{self.exclamation_point} Неправильный логин или пароль!Попробуйте снова')

    def authorization_token(self):
        while True:
            try:
                self.token = input(f'\n{self.plus} Введите токен:\n')
                if len(self.token) == 85:
                    vk = vk_api.VkApi(token=self.token)
                    info_account = vk.method('users.get', {})
                    fn = info_account[0]["first_name"]
                    ln = info_account[0]["last_name"]
                    print(f'\n{self.g}Аккаунт {fn} {ln} был успешно авторизован!{self.d}')
                    self.authorization_token_anticaptcha()
                    break
                else:
                    print(f'\n{self.exclamation_point} Ваш токен содержит {len(self.token)} символов, а должен 85.\nПоп'
                          f'робуйте снова')
            except:
                print(f'\n{self.exclamation_point} Ваш токен содержит ошибку, попробуйте ввести его снова!')

    def authorization_token_anticaptcha(self):
        while True:
            try:
                self.capt_question = int(input(f'\nУ вас есть токен и капча на anti-captcha.com?\n{self.g}[{self.d}1'
                                               f'{self.g}]{self.d} Нет. Если возникнет капча, буду вводить её ручками\n'
                                               f'{self.g}[{self.d}2{self.g}]{self.d} Да\n'))
                if self.capt_question == 1:
                    self.choice_of_answer()
                    break
                if self.capt_question == 2:
                    self.capt = input(f'\n{self.plus} Введите сюда ваш токен антикапчи:\n')
                    self.choice_of_answer()
                    break
                else:
                    print(f'\n{self.exclamation_point} Введите 1 или 2!')
            except:
                print(f'\n{self.exclamation_point} Введите число!')

    def choice_of_answer(self):
        while True:
            try:
                self.coa = int(input(f'\nВыберите способ отправки сообщения:\n{self.g}[{self.d}1{self.g}]{self.d} C пер'
                                     f'есылом\n{self.g}[{self.d}2{self.g}]{self.d} С ответом\n{self.g}[{self.d}3'
                                     f'{self.g}]{self.d} Просто отправка сообщения\n'))
                if self.coa > 0 and self.coa < 4:
                    self.choice_of_text()
                    break
                else:
                    print(f'\n{self.exclamation_point} Введите 1,2 или 3!')
            except:
                print(f'\n{self.exclamation_point} Введите число!')

    def choice_of_text(self):
        while True:
            try:
                self.cot = int(input(f'\nВаш бот будет будет слать сообщения с одним и тем же текстом?\n{self.g}['
                                     f'{self.d}1{self.g}]{self.d} Да\n{self.g}[{self.d}2{self.g}]{self.d} Нет\n'))
                if self.cot == 1:
                    self.text_input()
                    break
                if self.cot == 2:
                    self.choice_of_file()
                    break
                else:
                    print(f'\n{self.exclamation_point} Введите 1 или 2')
            except:
                print(f'\n{self.exclamation_point} Введите число!')

    def text_input(self):
        self.text = input(f'\n{self.plus} Введите текст, которым бот будет отвечать\n')
        self.who_to_answer()

    def choice_of_file(self):
        self.file = input(f'\n{self.plus} Введите путь до вашего файла с шаблонами: ')
        f = open(self.file, 'r', encoding='utf-8')
        self.a = f.read().splitlines()
        self.who_to_answer()

    def who_to_answer(self):
        while True:
            try:
                self.wto = int(input(f'\nКому мы будем отвечать?\n{self.g}[{self.d}1{self.g}]{self.d} Всем, кто напишет'
                                     f' сообщение\n{self.g}[{self.d}2{self.g}]{self.d} Всем, кто напишет сообщение в ко'
                                     f'нфе\n{self.g}[{self.d}3{self.g}]{self.d} Всем, кто напишет в лс\n{self.g}['
                                     f'{self.d}4{self.g}]{self.d} Определённому человеку/людям в лс\n{self.g}[{self.d}5'
                                     f'{self.g}]{self.d} Определённому человеку/людям в беседе\n{self.g}[{self.d}6'
                                     f'{self.g}]{self.d} В определённой беседе\n'))
                self.mode()
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!')

    def mode(self):
        while True:
            try:
                self.vibor = int(input(f'\nКак мы будем отвечать?\n{self.g}[{self.d}1{self.g}]{self.d} Сразу\n{self.g}['
                                       f'{self.d}2{self.g}]{self.d} Сначала определённый момент времени статус печатает'
                                       f' и потом отправка\n{self.g}[{self.d}3{self.g}]{self.d} Определённое время заде'
                                       f'ржки, потом отправка\n'))
                self.choice_on_mode()
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!')

    def choice_on_mode(self):
        if self.vibor == 1:
            self.work()
        if self.vibor == 2:
            while True:
                try:
                    self.second_typing = int(input(f'\n{self.plus} Введите сколько секунд бот будет печатать перед отпр'
                                                   f'авкой(от 1 до 10)\n'))
                    if self.second_typing > 0 and self.second_typing < 11:
                        self.work_typing()
                        break
                    else:
                        print(f'\n{self.exclamation_point} Введите число от 1 до 10!')
                except:
                    print(f'\n{self.exclamation_point} Введите число от 1 до 10!')
        if self.vibor == 3:
            while True:
                try:
                    self.second = int(input(f'\n{self.plus} Введите сколько будет задержка в секундах: '))
                    self.work_time()
                except:
                    print(f'\n{self.exclamation_point} Введите число!')
        else:
            print(f'\n{self.exclamation_point} Введите число от 1 до 3!')

    def captcha_handler(self, captcha):
        key = ImageToTextTask.ImageToTextTask(anticaptcha_key=self.capt,
                                              save_format='const').captcha_handler(captcha_link=captcha.get_url())
        return captcha.try_again(key['solution']['text'])

    def captcha_handler2(self, captcha):
        key = input(f"Введите капчу {captcha.get_url()}: ").strip()
        return captcha.try_again(key)

    def work(self):
        if self.capt_question == 1:
            self.vk = vk_api.VkApi(token=self.token, captcha_handler=self.captcha_handler2)
            self.longpoll = VkLongPoll(self.vk)
            self.auto_answer()
        else:
            self.vk = vk_api.VkApi(token=self.token, captcha_handler=self.captcha_handler)
            self.longpoll = VkLongPoll(self.vk)
            self.auto_answer()

    def work_typing(self):
        if self.capt_question == 1:
            self.vk = vk_api.VkApi(token=self.token, captcha_handler=self.captcha_handler2)
            self.longpoll = VkLongPoll(self.vk)
            self.auto_typing_answer()
        else:
            self.vk = vk_api.VkApi(token=self.token, captcha_handler=self.captcha_handler)
            self.longpoll = VkLongPoll(self.vk)
            self.auto_typing_answer()

    def work_time(self):
        if self.capt_question == 1:
            self.vk = vk_api.VkApi(token=self.token, captcha_handler=self.captcha_handler2)
            self.longpoll = VkLongPoll(self.vk)
            self.auto_time_answer()
        else:
            self.vk = vk_api.VkApi(token=self.token, captcha_handler=self.captcha_handler)
            self.longpoll = VkLongPoll(self.vk)
            self.auto_time_answer()

    def auto_answer(self):
        print(f'\n{self.g}Автоответчик начал свою работу!{self.d}')
        if self.wto == 1:   # отправлять сообщение всем
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                        'forward_messages': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                        'reply_to': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a),
                                        'forward_messages': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a),
                                        'reply_to': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a)
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 2:   # всем кто напишет сообщение в конфе
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 3:   # всем кто напишет в лс
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 4:   # определённому в лс
            a = input(f'\n{self.plus} Введите айдишники тех людей или человека, которому мы будем отвечать через пробел'
                      f'\nПример: 3241231 3898232 89832\nЕсли человек один, то просто вводим его айди.\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 5:   # определённому в конфе
            a = input(f'\n{self.plus} Введите айди человека которому бот будет отвечать. Если людей несколько, то вводи'
                      f'те через пробел\nПример: 3323245 1243212\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                                'forward_messages': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                                'reply_to': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a),
                                                'forward_messages': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a),
                                                'reply_to': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a)
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 6:   # в определённой беседе
            a = input(f'\n{self.plus} Введите айди беседы, где бот будет отвечать. Если бесед несколько, то вводите чер'
                      f'ез пробел\nПример: 21 43 83 76\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        else:
            print(f'\n{self.exclamation_point} Введите число от 1 до 6!')
            self.who_to_answer()

    def auto_typing_answer(self):
        print(f'\n{self.g}Автоответчик начал свою работу!{self.d}')
        if self.wto == 1:  # отправлять сообщение всем
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.setActivity', {
                                        'type': 'typing',
                                        'peer_id': event.peer_id
                                    })
                                    time.sleep(self.second_typing)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                        'forward_messages': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.setActivity', {
                                        'type': 'typing',
                                        'peer_id': event.peer_id
                                    })
                                    time.sleep(self.second_typing)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                        'reply_to': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.setActivity', {
                                        'type': 'typing',
                                        'peer_id': event.peer_id
                                    })
                                    time.sleep(self.second_typing)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.setActivity', {
                                        'type': 'typing',
                                        'peer_id': event.peer_id
                                    })
                                    time.sleep(self.second_typing)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a),
                                        'forward_messages': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.setActivity', {
                                        'type': 'typing',
                                        'peer_id': event.peer_id
                                    })
                                    time.sleep(self.second_typing)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a),
                                        'reply_to': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    self.vk.method('messages.setActivity', {
                                        'type': 'typing',
                                        'peer_id': event.peer_id
                                    })
                                    time.sleep(self.second_typing)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a)
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 2:  # всем кто напишет сообщение в конфе
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 3:  # всем кто напишет в лс
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 4:  # определённому в лс
            a = input(f'\n{self.plus} Введите айдишники тех людей или человека, которому мы будем отвечать через пробел'
                      f'\nПример: 3241231 3898232 89832\nЕсли человек один, то просто вводим его айди.\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 5:  # определённому в конфе
            a = input(f'\n{self.plus} Введите айди человека которому бот будет отвечать. Если людей несколько, то вводи'
                      f'те через пробел\nПример: 3323245 1243212\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.setActivity', {
                                                'type': 'typing',
                                                'peer_id': event.peer_id
                                            })
                                            time.sleep(self.second_typing)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                                'forward_messages': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.setActivity', {
                                                'type': 'typing',
                                                'peer_id': event.peer_id
                                            })
                                            time.sleep(self.second_typing)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                                'reply_to': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.setActivity', {
                                                'type': 'typing',
                                                'peer_id': event.peer_id
                                            })
                                            time.sleep(self.second_typing)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.setActivity', {
                                                'type': 'typing',
                                                'peer_id': event.peer_id
                                            })
                                            time.sleep(self.second_typing)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a),
                                                'forward_messages': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.setActivity', {
                                                'type': 'typing',
                                                'peer_id': event.peer_id
                                            })
                                            time.sleep(self.second_typing)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a),
                                                'reply_to': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.setActivity', {
                                                'type': 'typing',
                                                'peer_id': event.peer_id
                                            })
                                            time.sleep(self.second_typing)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a)
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 6:  # в определённой беседе
            a = input(f'\n{self.plus} Введите айди беседы, где бот будет отвечать. Если бесед несколько, то вводите чер'
                      f'ез пробел\nПример: 21 43 83 76\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        self.vk.method('messages.setActivity', {
                                            'type': 'typing',
                                            'peer_id': event.peer_id
                                        })
                                        time.sleep(self.second_typing)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        else:
            print(f'\n{self.exclamation_point} Введите число от 1 до 6!')
            self.who_to_answer()

    def auto_time_answer(self):
        print(f'\n{self.g}Автоответчик начал свою работу!{self.d}')
        if self.wto == 1:  # отправлять сообщение всем
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    time.sleep(self.second)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                        'forward_messages': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    time.sleep(self.second)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                        'reply_to': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    time.sleep(self.second)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': self.text,
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    time.sleep(self.second)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a),
                                        'forward_messages': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    time.sleep(self.second)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a),
                                        'reply_to': event.message_id
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    time.sleep(self.second)
                                    self.vk.method('messages.send', {
                                        'random_id': 0,
                                        'peer_id': event.peer_id,
                                        'message': random.choice(self.a)
                                    })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 2:  # всем кто напишет сообщение в конфе
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 3:  # всем кто напишет в лс
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_user:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 4:  # определённому в лс
            a = input(f'\n{self.plus} Введите айдишники тех людей или человека, которому мы будем отвечать через пробел'
                      f'\nПример: 3241231 3898232 89832\nЕсли человек один, то просто вводим его айди.\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if str(event.peer_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'user_id': event.user_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 5:  # определённому в конфе
            a = input(f'\n{self.plus} Введите айди человека которому бот будет отвечать. Если людей несколько, то вводи'
                      f'те через пробел\nПример: 3323245 1243212\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            time.sleep(self.second)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                                'forward_messages': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            time.sleep(self.second)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                                'reply_to': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            time.sleep(self.second)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': self.text,
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            time.sleep(self.second)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a),
                                                'forward_messages': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        if event.raw[6]['from'] in b:
                                            time.sleep(self.second)
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a),
                                                'reply_to': event.message_id
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat:
                                        time.sleep(self.second)
                                        if event.raw[6]['from'] in b:
                                            self.vk.method('messages.send', {
                                                'random_id': 0,
                                                'chat_id': event.chat_id,
                                                'message': random.choice(self.a)
                                            })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        if self.wto == 6:  # в определённой беседе
            a = input(f'\n{self.plus} Введите айди беседы, где бот будет отвечать. Если бесед несколько, то вводите чер'
                      f'ез пробел\nПример: 21 43 83 76\n')
            b = a.split(' ')
            if self.cot == 1:  # слать сообщения с одним и тем же текстом
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': self.text,
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')

            else:  # слать шаблоны
                if self.coa == 1:  # способ отправки (пересыл)
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'forward_messages': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                elif self.coa == 2:  # ответ
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a),
                                            'reply_to': event.message_id
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
                else:  # просто сообщение
                    while True:
                        try:
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                                    if event.from_chat and str(event.chat_id) in b:
                                        time.sleep(self.second)
                                        self.vk.method('messages.send', {
                                            'random_id': 0,
                                            'chat_id': event.chat_id,
                                            'message': random.choice(self.a)
                                        })
                        except Exception as e:
                            print(f'\n{self.exclamation_point} произошла ошибка:\n{e}')
        else:
            print(f'\n{self.exclamation_point} Введите число от 1 до 6!')
            self.who_to_answer()


if __name__ == '__main__':
    base = Base()
    base.intro()