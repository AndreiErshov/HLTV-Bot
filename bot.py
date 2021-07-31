if __name__ != '__main__':
    exit("Can't import this script")

from dispatcher import longpoll, vk
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from asyncio import run
import parser

start_keyboard = VkKeyboard(one_time=False)
start_keyboard.add_button('Получить ТОП-30 команд', color=VkKeyboardColor.PRIMARY)
start_keyboard.add_line()
start_keyboard.add_button('Узнать предстоящие турниры', color=VkKeyboardColor.POSITIVE)
start_keyboard.add_button('Узнать проходящие турниры', color=VkKeyboardColor.NEGATIVE)

event_keyboard = VkKeyboard(one_time=False)
event_keyboard.add_button('Все', color=VkKeyboardColor.POSITIVE)
event_keyboard.add_button('Мажоры', color=VkKeyboardColor.PRIMARY)
event_keyboard.add_line()
event_keyboard.add_button('LAN Международные', color=VkKeyboardColor.PRIMARY)
event_keyboard.add_button('LAN Региональные', color=VkKeyboardColor.PRIMARY)
event_keyboard.add_button('LAN Локальные', color=VkKeyboardColor.PRIMARY)
event_keyboard.add_line()
event_keyboard.add_button('Онлайн', color=VkKeyboardColor.PRIMARY)
event_keyboard.add_button('Найти ивенты')

cmd_handlers = {}
states = {}
def_msg = "Выберите нужный пункт"


def add_handler(func, *args):
    for i in args:
        cmd_handlers[i] = func


async def start_command(msg):
    peer = msg['peer_id']
    send_message(def_msg, peer, keyboard=start_keyboard.get_keyboard())


async def top_command(msg):
    peer = msg['peer_id']
    result = await parser.get_top()
    send_message("ТОП-30 HLTV: \n" + ', '.join(result).replace('.', ' '), peer)


async def upcoming_command(msg):
    peer = msg['peer_id']
    states[peer] = ["upcoming", []]
    send_message(def_msg, peer, keyboard=event_keyboard.get_keyboard())
    # send_message("Предстоящие турниры: \n" + ', '.join(result).replace('.', ' '), peer)


async def incoming_command(msg):
    peer = msg['peer_id']
    states[peer] = ["incoming", []]
    send_message(def_msg, peer, keyboard=event_keyboard.get_keyboard())

def send_message(msg, peer, keyboard=None):
    vk.messages.send(
        keyboard=keyboard,
        random_id=get_random_id(),
        message=msg,
        peer_id=peer
    )


async def main_loop():
    print("Bot is working!")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not event.from_chat:
                text = event.object.message['text']
                if text in cmd_handlers:
                    await cmd_handlers[text](event.object.message)


async def add_type(msg, match_type):
    peer = msg['peer_id']
    if peer in states:
        if match_type == "Все" or match_type == "Найти ивенты":
            tournir_type = None
            result = None
            types = None
            if match_type == "Все":
                types = ["Всё"]
            else:
                types = states[peer][1]
            if states[peer][0] == "upcoming":
                tournir_type = "Предстоящие"
                result = await parser.get_upcoming_events(types)
            else:
                tournir_type = "Проходящие"
                result = await parser.get_incoming_events(types)
            del states[peer]
            send_message(tournir_type + " турниры: \n" + ', '.join(result), peer,
                         keyboard=start_keyboard.get_keyboard())
        else:
            states[peer][1].append(match_type)
            send_message("Выбрано", peer)


add_handler(start_command, "Начать")
add_handler(top_command, "Получить ТОП-30 команд")
add_handler(upcoming_command, "Узнать предстоящие турниры")
add_handler(incoming_command, "Узнать проходящие турниры")

add_handler(lambda c: add_type(c, "Все"), "Все")
add_handler(lambda c: add_type(c, "Мажоры"), "Мажоры")
add_handler(lambda c: add_type(c, "LAN Международные"), "LAN Международные")
add_handler(lambda c: add_type(c, "LAN Региональные"), "LAN Региональные")
add_handler(lambda c: add_type(c, "LAN Локальные"), "LAN Локальные")
add_handler(lambda c: add_type(c, "Онлайн"), "Онлайн")
add_handler(lambda c: add_type(c, "Найти ивенты"), "Найти ивенты")
run(main_loop())
