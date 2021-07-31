from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
import config

vk_session = VkApi(token=config.BOT_TOKEN)

longpoll = VkBotLongPoll(vk_session, '206188548')
vk = vk_session.get_api()
