from bs4 import BeautifulSoup
import aiohttp


async def get_html_soup(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return BeautifulSoup(html, "html.parser")


async def get_top():
    soup = await get_html_soup('https://www.hltv.org/ranking/teams')
    return [i.text.replace('.', ' ') for i in soup.find_all("span", {"class": "name"})]


async def get_url(types):
    types_array = []
    if "Все" in types:
        return "https://www.hltv.org/events#tab-ALL"
    if "Мажоры" in types:
        types_array.append("eventType=MAJOR")
    if "LAN Международные" in types:
        types_array.append("eventType=INTLLAN")
    if "LAN Региональные" in types:
        types_array.append("eventType=REGIONALLAN")
    if "LAN Локальные" in types:
        types_array.append("ventType=LOCALLAN")
    if "Онлайн" in types:
        types_array.append("eventType=ONLINE")
    if len(types_array) < 1:
        return None
    else:
        return "https://www.hltv.org/events?" + '&'.join(types_array) + "#tab-ALL"


async def get_upcoming_events(types):
    url = await get_url(types)
    if url is None:
        return []
    soup = await get_html_soup(url)
    return [i.text.replace('.', ' ') for i in soup.select(".big-event-info > .info > .big-event-name,"
                                                          ".col-value > .text-ellipsis")]


async def get_incoming_events(types):
    url = await get_url(types)
    if url is None:
        return []
    soup = await get_html_soup(url)
    result = []
    html_select = soup.select(".event-name-col > .event-name-small > .text-ellipsis")
    for i in html_select:
        edited = i.text
        if edited not in result:
            result.append(edited.replace('.', ' '))
    return result
