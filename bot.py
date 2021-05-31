# VK BOT 2021 - Простой менеджер бесед. 
# Версия 0.0.1 - 21.05.2021
# author: iframe

import vk_api, config, sys, time, colorama, sqlite3, subsidiary
from requests.models import Response
from vk_api.bot_longpoll import VkBotEvent, VkBotEventType, VkBotLongPoll, VkBotMessageEvent
from datetime import datetime
from vk_api.exceptions import VkToolsException
from vk_api.vk_api import VkApi, VkApiMethod
from vk_api.utils import get_random_id
from bot_func import *
from colorama import Fore, Style


Key = config.key
GroupID = config.group_id

colorama.init()

vk_session = vk_api.VkApi(token=Key)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GroupID, 30)
print(f'Авторизация бота ({Key})')
print(Fore.GREEN + '>>> Логи:' + Style.RESET_ALL)

for event in longpoll.listen():

    if event.type == VkBotEventType.MESSAGE_NEW:

        request = event.object['message'].get('text')
        user_id = event.object['message'].get('from_id')
        peer_id = event.object['message'].get('peer_id')
        msg_id = event.object['message'].get('id')
        vk = session_api

        if request == "/help" and event.from_chat: #event.from_chat — проверяет, если написали сообщение пришло от пользователя в чате
            """ send_message(vk, peer_id, 
            f'{subsidiary.i} Вспомогательные команды:\n\n'
            '/ban @пользователь <причина> <срок> — забанить пользователя в беседе\n'
            '/kick @пользователь <причина> — исключить пользователя из беседы\n'
            '/link — получить ссылку на приглашение в беседу\n'
            '/clear — удалить сообщения за последние время\n'
            '/warn @пользователь — выдать предупреждение пользователю беседы\n'
            '/setting <параметр> <значение> — изменить определённый параметр беседы\n') """
            send_message(vk, peer_id, 'Команды для бота: vk.cc/c2rj3N')
            
        #ban / unban
        if request[0:5] == "/ban ":
            ban(vk, event)
        
        if request[0:7] == "/unban ":
            unban(vk, event)

        #kick
        if request[0:6] == "/kick ":
            kick(vk, event)

        #link
        if request == '/link':
            link = givemelink(vk, peer_id, group_id=GroupID)['link']
            send_message(vk, peer_id, f'&#128279; {link}')
             
        # Логи

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
    
            chat_id = event.chat_id
            user_id = event.object['message'].get('from_id')
            firstName = vk.users.get(user_id=user_id)[0]['first_name']
            lastName = vk.users.get(user_id=user_id)[0]['last_name']
            chat = vk.messages.getConversationsById(peer_ids=peer_id)
            nameChat = chat['items'][0]['chat_settings']['title']
            text = event.object['message'].get('text')

            time = datetime.now().strftime('%H:%M:%S')

            print('')
            print('========================================')
            print(f'[{time}]')
            print(f'Беседа № {chat_id}')
            print(f'Название: {nameChat}')
            print(f'Имя: {firstName}')
            print(f'Фамилия: {lastName}')
            print(f'ID: {user_id}')
            print(f'Сообщение: {text}')
            print(f'Событие: {event.type}')
            print('========================================')