#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import vk_api
from threading import Thread
from colorama import Style, Fore
from vk_api.longpoll import VkEventType, VkLongPoll


class Main():

    def __init__(self):
        self.y = Fore.LIGHTYELLOW_EX     # ярко-жёлтый цвет
        self.g = Fore.LIGHTGREEN_EX     # ярко-зелёный цвет
        self.r = Fore.LIGHTRED_EX     # ярко-красный цвет
        self.d = Style.RESET_ALL     # очистка цветов
        self.plus = f'{self.g}[{self.d} + {self.g}]{self.d}'
        self.exclamation_point = f'{self.r}[{self.d} ! {self.r}]{self.d}'

    def intro(self):
        print(''' █████╗ ███╗   ██╗████████╗██╗██╗  ██╗██╗ ██████╗██╗  ██╗
██╔══██╗████╗  ██║╚══██╔══╝██║██║ ██╔╝██║██╔════╝██║ ██╔╝
███████║██╔██╗ ██║   ██║   ██║█████╔╝ ██║██║     █████╔╝ 
██╔══██║██║╚██╗██║   ██║   ██║██╔═██╗ ██║██║     ██╔═██╗ 
██║  ██║██║ ╚████║   ██║   ██║██║  ██╗██║╚██████╗██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝\n''')
        self.nachalo()

    def nachalo(self):
        while True:
            try:
                scenario_selection = int(input(f'Выберите сценарий:\n{self.y}[{self.d}1{self.y}]{self.d} Запуск антикик'
                                               f'а\n{self.y}[{self.d}2{self.y}]{self.d} Редактирование конфига\n'
                                               f'{self.y}[{self.d}3{self.y}]{self.d} Создание конфига\n'))
                if scenario_selection == 1:
                    self.antikickf()
                    break
                elif scenario_selection == 2:
                    self.redacted()
                    break
                elif scenario_selection == 3:
                    self.number_of_accounts()
                    break
                else:
                    print(f'{self.exclamation_point} Введите 1,2 или 3!')
                    continue
            except:
                print(f'{self.exclamation_point} Введите число!\n')
                continue

    def redacted(self):
        while True:
            try:
                print('Выберите действие:')
                red_choice = int(input(f'{self.g}[{self.d}1{self.g}]{self.d} Добавление других токенов\n{self.g}['
                                       f'{self.d}2{self.g}]{self.d} Добавление других айдишников\n{self.g}[{self.d}3'
                                       f'{self.g}]{self.d} Удаление и создание нового конфига\n'))
                if red_choice == 1:
                    self.add_new_token()
                    break
                if red_choice == 2:
                    self.id_function()
                    break
                if red_choice == 3:
                    self.del_config()
                    break
                else:
                    print(f'{self.exclamation_point} Введите 1,2 или 3!')
                    continue
            except:
                print(f'{self.exclamation_point} Введите число!\n')
                continue

    def del_config(self):
        f = open('token.txt', 'w')
        f.close()
        f = open('id.txt', 'w')
        f.close()
        self.number_of_accounts()

    def add_new_token(self):
        while True:
            try:
                self.quantity2 = int(input('Введите количество аккаунтов, что будут добавлять: '))
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!\n')
                continue
        for self.i2 in range(self.quantity2):
            self.choice_of_authorization2()

    def choice_of_authorization2(self):
        while True:
            try:
                self.authorization_through_what2 = int(input(f'\nЧерез что будем авторизовывать аккаунт №{self.i2 + 1}?'
                                                             f'\n{self.g}[{self.d}1{self.g}]{self.d} Через токен\n'
                                                             f'{self.g}[{self.d}2{self.g}]{self.d} Через логин и пароль'
                                                             f'\n'))
                self.add_token2()
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!')
                continue

    def add_token2(self):
        if self.authorization_through_what2 == 1:
            while True:
                try:
                    token = input(f'{self.plus} Введите токен №{self.i2 + 1} аккаунта:\n')
                    if len(token) == 85:
                        vk = vk_api.VkApi(token=token)
                        info_account = vk.method('users.get', {})
                        id = info_account[0]["id"]
                        print(f'\n{self.g}[id{id}]{self.d} - был успешно добавлен!')
                        with open('token.txt', 'a') as file_token:
                            file_token.writelines(f'{token}\n')
                            file_token.close()
                        with open('id.txt', 'a') as file_id:
                            file_id.writelines(f'{id}\n')
                            file_id.close()
                        i_plus_one = self.i2 + 1
                        if i_plus_one == self.quantity2:
                            self.end_config()
                        else:
                            break
                    else:
                        print(f'{self.exclamation_point} Ваш токен содержит {len(token)} символов, а должен 85.\nПопроб'
                              f'уйте снова')
                        continue
                except:
                    print(f'{self.exclamation_point} Ваш токен содержит ошибку, попробуйте ввести его снова!')

        if self.authorization_through_what2 == 2:
            while True:
                try:
                    number = input(f'\n{self.plus} Введите номер: ')
                    password = input(f'{self.plus} Введите пароль: ')
                    url = f"https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqy" \
                          f"rnABp8ncuU&username={number}&password={password}"
                    ke = requests.get(url).json()
                    token = ke['access_token']
                    vk = vk_api.VkApi(token=token)
                    info_account = vk.method('users.get', {})
                    id = info_account[0]["id"]
                    print(f'\n{self.g}[id{id}]{self.d} - был успешно добавлен!')
                    with open('token.txt', 'a') as file_token:
                        file_token.writelines(f'{token}\n')
                        file_token.close()
                    with open('id.txt', 'a') as file_id:
                        file_id.writelines(f'{id}\n')
                        file_id.close()
                    i_plus_one = self.i2 + 1
                    if i_plus_one == self.quantity2:
                        self.end_config()
                    else:
                        break
                except:
                    print(f'{self.exclamation_point} Неправильный логин или пароль!\nПопробуйте снова')
                    continue
        else:
            print(f'{self.exclamation_point} Введите 1 или 2!')
            self.choice_of_authorization2()

    def number_of_accounts(self):
        while True:
            try:
                self.quantity = int(input('Введите количество аккаунтов, что будут добавлять: '))
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!\n')
                continue
        for self.i in range(self.quantity):
            self.choice_of_authorization()

    def choice_of_authorization(self):
        while True:
            try:
                self.authorization_through_what = int(input(f'\nЧерез что будем авторизовывать аккаунт №{self.i + 1}?\n'
                                                            f'{self.g}[{self.d}1{self.g}]{self.d} Через токен\n{self.g}'
                                                            f'[{self.d}2{self.g}]{self.d} Через логин и пароль\n'))
                self.add_token()
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!')
                continue

    def add_token(self):
        if self.authorization_through_what == 1:
            while True:
                try:
                    token = input(f'{self.plus} Введите токен №{self.i + 1} аккаунта:\n')
                    if len(token) == 85:
                        vk = vk_api.VkApi(token=token)
                        info_account = vk.method('users.get', {})
                        id = info_account[0]["id"]
                        print(f'{self.g}[id{id}]{self.d} - был успешно добавлен!')
                        with open('token.txt', 'a') as file_token:
                            file_token.writelines(f'{token}\n')
                            file_token.close()
                        with open('id.txt', 'a') as file_id:
                            file_id.writelines(f'{id}\n')
                            file_id.close()
                        i_plus_one = self.i + 1
                        if i_plus_one == self.quantity:
                            self.id_function()
                        else:
                            break
                    else:
                        print(f'{self.exclamation_point} Ваш токен содержит {len(token)} символов, а должен 85.\nПопроб'
                              f'уйте снова')
                        continue
                except:
                    print(f'{self.exclamation_point} Ваш токен содержит ошибку, попробуйте ввести его снова!')

        elif self.authorization_through_what == 2:
            while True:
                try:
                    number = input(f'\n{self.plus} Введите номер: ')
                    password = input(f'{self.plus} Введите пароль: ')
                    url = f"https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqy" \
                          f"rnABp8ncuU&username={number}&password={password}"
                    ke = requests.get(url).json()
                    token = ke['access_token']
                    vk = vk_api.VkApi(token=token)
                    info_account = vk.method('users.get', {})
                    id = info_account[0]["id"]
                    print(f'\n{self.g}[id{id}]{self.d} - был успешно добавлен!')
                    with open('token.txt', 'a') as file_token:
                        file_token.writelines(f'{token}\n')
                        file_token.close()
                    with open('id.txt', 'a') as file_id:
                        file_id.writelines(f'{id}\n')
                        file_id.close()
                    i_plus_one = self.i + 1
                    if i_plus_one == self.quantity:
                        self.end_config()
                    else:
                        break
                except:
                    print(f'{self.exclamation_point} Неправильный логин или пароль!\nПопробуйте снова')
                    continue
        else:
            print(f'{self.exclamation_point} Введите 1 или 2!')
            self.choice_of_authorization()

    def id_function(self):
        while True:
            try:
                self.quantity_id = int(input('Введите какое количество аккаунтов будем добавлять(аккаунты что будут доб'
                                             'авлять - не в счёт. Они уже добавлены.)\nЕсли вам не нужно добавлять друг'
                                             'их людей при кике, введите 0\n'))
                break
            except:
                print(f'\n{self.exclamation_point} Введите число!\n')
                continue
        for self.a in range(self.quantity_id):
            self.add_id()

    def add_id(self):
        if self.quantity_id == 0:
            self.end_config()
        else:
            while True:
                try:
                    self.id_man = int(input(f'{self.plus} Введите айди №{self.a + 1}, который будем добавлять при кике '
                                            f'(просто цифры): '))
                    with open("token.txt") as file_token:
                        token = file_token.read().splitlines()
                        vk = vk_api.VkApi(token=token[0])
                        info_account = vk.method('users.get', {
                            'user_ids': self.id_man
                        })
                        id = info_account[0]["id"]
                        first_name = info_account[0]["first_name"]
                        last_name = info_account[0]["last_name"]
                        print(f'\n{self.g}[id{id} {first_name} {last_name}]{self.d} - был успешно добавлен!\n')
                        with open('id.txt', 'a') as file_id:
                            file_id.writelines(f'{self.id_man}\n')
                            file_id.close()
                            file_token.close()
                    a_plus_one = self.a + 1
                    if a_plus_one == self.quantity_id:
                        self.end_config()
                    else:
                        break
                except:
                    print(f'\n{self.exclamation_point} Ваш айди содежит ошибку, попробуйте снова.\n')
                    continue

    def end_config(self):
        print(f'{self.g}Создание конфига завершено!{self.d}')
        self.nachalo()

    def antikickf(self):
        print(f'\n{self.g}Антикик запущен{self.d}')
        with open("id.txt") as file_id:
            ids = file_id.read().splitlines()
            file_id.close()
        with open("token.txt") as file_token:
            tokens = file_token.read().splitlines()
            file_token.close()
        for token in tokens:
            t = Antikick(token, ids)
            t.start()


class Antikick(Thread):
    def __init__(self, token, ids):
        Thread.__init__(self)
        self.token_ak = token
        self.id_ak = ids

    def run(self):
        vk = vk_api.VkApi(token=self.token_ak)
        longpoll = VkLongPoll(vk)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if 'source_act' in event.raw[6]:
                    if event.raw[6]['source_act'] == 'chat_kick_user':
                        if event.raw[6]['source_mid'] in self.id_ak:
                            try:
                                vk.method('messages.addChatUser', {
                                    'chat_id': event.chat_id,
                                    'user_id': event.raw[6]['source_mid']
                                })
                            except:
                                pass


if __name__ == '__main__':
    main = Main()
    main.intro()
