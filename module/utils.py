import asyncio
import aiohttp
import random
import json
from .config import HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY,USER_AGENTS

LOOP_CRAWLER = asyncio.get_event_loop()
LOOP_LISTENER = asyncio.get_event_loop()

async def _get_page(url, sleep):
    """
    获取并返回网页内容
    """
    HEADERS["User-Agent"] = random.choice(USER_AGENTS)
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.sleep(sleep)
            async with session.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT
            ) as resp:
                return await resp.json()
        except TimeoutError:
            return ""


async def _run_all (request_url, sleep):
    url_list = list(map(lambda x: request_url + '?limit=250&page=' + str(x), range(1, 36)))
    tasks = [_get_page(url , sleep) for url in url_list]
    return await asyncio.gather(*tasks)


def requests(url, sleep= REQUEST_DELAY):
    """
    请求方法，用于获取网页内容

    :param url: 请求链接
    :param sleep: 延迟时间（秒）
    """
    json_data = LOOP_CRAWLER.run_until_complete(_run_all(url, sleep))
    if json_data:
        return json_data


async def _post_page(url,payload,sleep):
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.sleep(sleep)
            async with session.post(
                    url, data=json.dumps(payload),
                    headers={"Content-Type": "application/json"}
            )as resp:
                return await resp.text()
        except TimeoutError:
            return ""


def discord_push(url, payload, sleep=REQUEST_DELAY):
    json_data = LOOP_LISTENER.run_until_complete(_post_page(url,payload,sleep))
    if json_data:
        return json_data



class Store:
    storeDict = {'palace': 'http://shop-usa.palaceskateboards.com',
                 'epsk8': 'https://www.empireskate.com.au',
                 'apc-us': 'https://www.apc-us.com',
                 'jjjjound': 'https://jjjjound.com',
                 'ronin': 'http://www.ronindivision.com',
                 'bnrb': 'http://burnrubbersneakers.com',
                 'yzsp': 'http://shop.yeezysupply.com',
                 'kith': 'http://kithnyc.com',
                 'cncpts': 'http://shop.cncpts.com',
                 'bdga': 'http://shop.bdgastore.com',
                 'xbih': 'http://www.xhibition.co',
                 'sole': 'http://soleclassics.com',
                 'rise': 'http://rise45.com',
                 'donc': 'http://shopjustdon.myshopify.com',
                 'rsvp': 'https://rsvpgallery.com',
                 'blds': 'http://www.blendsus.com',
                 'blkmkt': 'http://www.blkmkt.us',
                 'notre': 'http://www.notre-shop.com',
                 'union': 'https://store.unionlosangeles.com',
                 'nice': 'https://shopnicekicks.com',
                 'unkw': 'http://americanrag.com',
                 'nomad': 'http://nomadshop.net',
                 'lvsd': 'http://www.deadstock.ca',
                 'havn': 'http://shop.havenshop.ca',
                 'prop': 'http://apropersite.com',
                 'ftsb': 'http://www.featuresneakerboutique.com',
                 'ctsd': 'https://courtsidesneakers.com',
                 'slcs': 'http://soleclassics.com',
                 'cbshop': 'http://www.cityblueshop.com',
                 'packer': 'http://packershoes.com',
                 'stafrd': 'http://www.saintalfred.com',
                 'exbt': 'http://shop.extrabutterny.com',
                 'dash': 'https://shopdashonline.com',
                 'oth': 'https://offthehook.ca',
                 'fog': 'https://fearofgod.com',
                 'tdco': 'https://todayclothing.com',
                 'excu': 'https://shop.exclucitylife.com'}


    def __init__(self, name):
        self.storeName = name
        if name in self.storeDict.keys():
            self.storeHome = self.storeDict[self.storeName]
        else:
            self.storeHome = 'https://+www. ' + name + '.com'
        self.json_url = self.storeHome + '/products.json'
        self.xml_url = self.storeHome + '/sitemap_products_1.xml'


    #return embed discord payload data

    def json_embed(self,payload):
        data = {"content": "", "username": "ShopPy Bot", "embeds": []}
        embed = {"title": payload["title"],
                 "url": self.storeHome + '/product/' + payload["handle"], "timestamp": payload["updated_at"],
                 "footer": {"text": "ShopPy Bot"}, "thumbnail": {},
                 "fields": [{"name": "price", "value": payload["variants"][0]["price"]},
                            {"name": "sizes", "value": " ".join(
                                ["[" + x["title"] + "](" + self.storeHome + "/cart/" + str(x["id"]) + ":1)" for x in
                                 payload["variants"]])}]}
        try:
            embed["thumbnail"]["url"] = payload["images"][0]["src"]
        except IndexError:
            embed["thumbnail"] = {}
        data["embeds"].append(embed)
        return data

    @staticmethod
    def add_store(name, link):
        assert link.startswith('http'), 'invalid url address'
        Store.storeDict[name] = link
        return 'store {} has been successfully added'.format(name)

    @staticmethod
    def remove_store(name):
        return Store.storeDict.pop(name, "store is not existed")

    def cart_url(self, variant, quantity):
        full_url = self.storeHome + '/cart/' + variant + ':' + quantity
        return full_url