# Файл со всеми функциями для бота
# Модифицировать/добавлять функции бота здесь

import re
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id
import vk_api, config, sys, time, colorama, random, sqlite3, re, subsidiary

GroupID = config.group_id

#https://vk.com/dev/messages.send
def send_message(vk, peer_id, message, sticker_id=None, attachment=None):
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        message=message,
        sticker_id=sticker_id,
        attachment=attachment
    )

#https://vk.com/dev/messages.createChat
def create_chat(vk, user_ids, title, group_id):
    return vk.messages.createChat(
        user_ids=user_ids,
        title=title,
        group_id=group_id
    )
#https://vk.com/dev/messages.getInviteLink
def givemelink(vk, peer_id, group_id):
    return vk.messages.getInviteLink(
        peer_id=peer_id,
        group_id=group_id
    )

#https://vk.com/dev/messages.removeChatUser
def ban(vk, event):
    target = event.object['message'].get('text')[5:]
    nkd = target.split('|')[0]
    ban_id = re.findall(r'id(.*)', nkd)[0]

    re_reason = '.*?] (\w+) (\w+)'

    i = f"{target}"
    string = i.split()
    print(string)

    if string[1] and string[2] == 0:
        print('NONE')

    first_name = vk.users.get(user_id=ban_id)[0]['first_name']
    last_name = vk.users.get(user_id=ban_id)[0]['last_name']
    peer_id = event.object['message'].get('peer_id')
    user_id = event.object['message'].get('from_id')
    chat_id = event.chat_id

    #sqlite3

    sqlite = sqlite3.connect('BOT_DATABASE.db')
    cursor = sqlite.cursor()

    RE = """INSERT INTO BAN_USERS (ID, CHAT_ID, FIRST_NAME, LAST_NAME, REASON, TERM, WHO) VALUES (?,?,?,?,?,?,?)"""
    cursor.execute(RE, (str(ban_id), str(chat_id), str(first_name), str(last_name), str(reason), '29.05.2021', str(user_id)))
    sqlite.commit()

    #vk.messages.removeChatUser(chat_id=chat_id, user_id=str(ban_id))
    send_message(vk, peer_id, f'☑ {first_name} {last_name} был забанен в беседе №{chat_id} по причине: {reason}, на срок {term} дней')

def unban(vk, event):

    target = event.object['message'].get('text')[7:]

    peer_id = event.object['message'].get('peer_id')
    user_id = event.object['message'].get('from_id')
    chat_id = event.chat_id

    #sqlite3

    sqlite = sqlite3.connect('BOT_DATABASE.db')
    cursor = sqlite.cursor()

    FI = """SELECT ID FROM BAN_USERS WHERE FIRST_NAME = ? OR LAST_NAME = ? AND CHAT_ID = ?"""
    cursor.execute(FI, (target, target, str(chat_id),))
    user = cursor.fetchall()
    print(user)

    RE = """DELETE FROM BAN_USERS WHERE ID = ? AND CHAT_ID = ?"""
    cursor.execute(RE, (user[0][0], str(chat_id)),)
    sqlite.commit()

    first_name = vk.users.get(user_id=user[0][0])[0]['first_name']
    last_name = vk.users.get(user_id=user[0][0])[0]['last_name']

    send_message(vk, peer_id, f'☑ {first_name} {last_name} был разбанен в беседе №{chat_id}')

def kick(vk, event):
    try:
        target = event.object['message'].get('text')[6:]
        nkd = target.split('|')[0]
        ban_id = re.findall(r'id(.*)', nkd)[0]
        re_reason = '.*?] (\w+)'
        reason = re.search(re_reason, target).group(1)

        first_name = vk.users.get(user_id=ban_id)[0]['first_name']
        last_name = vk.users.get(user_id=ban_id)[0]['last_name']
        peer_id = event.object['message'].get('peer_id')
        chat_id = event.chat_id

        vk.messages.removeChatUser(chat_id=chat_id, user_id=str(ban_id))
        send_message(vk, peer_id, f'☑ {first_name} {last_name} был исключён из беседы №{chat_id} по причине: {reason}')
    except:
        peer_id = event.object['message'].get('peer_id')
        if config.dg == 1: #debug mode
            send_message(vk, peer_id, message='{}'.format(sys.exc_info()[1]))
        send_message(vk, peer_id, f'{subsidiary.error_kick}')

""" def warn(vk, event):
    try:
        target = event.object['message'].get('text')[6:]
        nkd = target.split('|')[0]
        warn_id = re.findall(r'id(.*)', nkd)[0]
        re_reason = '.*?] (\w+)'
        reason = re.search(re_reason, target).group(1)

        first_name = vk.users.get(user_id=warn_id)[0]['first_name']
        last_name = vk.users.get(user_id=warn_id)[0]['last_name']
        peer_id = event.object['message'].get('peer_id')
        chat_id = event.chat_id

        sqlite = sqlite3.connect('BOT_DATABASE.db')
        cursor = sqlite.cursor()


        

        vk.messages.removeChatUser(chat_id=chat_id, user_id=str(warn_id))
        send_message(vk, peer_id, f'☑ {first_name} {last_name}: предупрежение №{w} по причине: {reason}')
 """