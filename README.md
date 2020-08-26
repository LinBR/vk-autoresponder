# vk-autoresponder
Навороченный автоответчик вк с гибкой настройкой
## Подробное описание
Что представляет из себя данный скрипт?  
### Автоотвечика вк с несколькими выборами запуска.  
1. Отвечать везде, где придёт сообщение
2. Отвечать только в конфе
3. Отвечать только в определённой конфе
4. Отвечать только в лс
5. Отвечать только в лс определённому человеку/людям
6. Отвечать определённым людям в конфе  
### Также вы можете выбрать то, как отвечать  
1. Пересылом
2. Ответом на сообщение
3. Простая отправка сообщения  
### И, конечно же, как отправлять  
1. Сразу же, как придёт сообщение
2. Через некоторое время с набором текстом
3. Через просто определённое время
## Как пользоваться?  
1.Для того, чтобы пользоваться скриптом, нам нужно там авторизоваться(ого), для этого мы идём получать токен на сайте https://vkhost.github.io/ через кейт мобайл, либо авторизовываемся через пароль и логин(работает нестабильно)  
2. Далее нам нужно выбрать как быть с капчей, если она случится. Либо мы даём скрипту свой токен с капчей https://anti-captcha.com/, либо соглашаемся на ручной ввод.  
3. Выбираем способ отправки сообщения  
4. Выбираем как бот будет отвечать(либо одной фразой, либо сразу  нескольколькими)  
5. И смотря от того, что вы выбрали, вводим вашу фразу, либо вводим путь к вашему файлику с этими фразами  
6. Выбираем где бот будет отвечать  
7. Далее выбираем задержку сообщений  
8. Всё  
## Как скачать?
### TERMUX
1. Для скрипта нужен питон, скачиваем  
pkg install python 
2. Чтобы скачать скрипт, нужен гит, его тоже скачиваем  
pkg install git
3. Теперь скачиваем сам скрипт  
git clone https://github.com/LinBR/vk-autoresponder
4. Переходим в папку со скриптом  
cd vk-autoresponder
5. Скачиваем модули, что использует скрипт  
 pip install -r requirements.txt
6. Запуск скрипта  
python auto_responder.py
### Linux
1. Скачиваем скрипт  
git clone https://github.com/LinBR/vk-autoresponder
2. Переходим в папку со скриптом  
cd vk-autoresponder
3. Скачиваем все зависимости, которые использует бот  
 pip install -r requirements.txt
4. Запуск скрипта  
python auto_responder.py
## Автор
Telegram: https://t.me/Lin089  
Discord: sueta.....#8453  
Vk: sosatb
