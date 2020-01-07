from datetime import datetime, timedelta

import pymongo

from .config import MONGODB_PORT, MONGODB_HOST, DBNAME
from .logger import logger
from .utils import discord_push

webhook_url = 'https://discordapp.com/api/webhooks/645273198434451467/EP8c2EotIhryfOARFJtHpohAM8z_-AN9VRmnRUzwPtMryYLRnA7Dryf6olC-KDMTATWk'
conn = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[DBNAME]

class listener:

    @staticmethod
    def listener_run(task):
        logger.info(" Listener working ")
        store = task.store
        kw = task.keyword.split(',')
        if len(kw) is not 0:
            pkw = [s[1:] for s in kw if '+' in s]
            nkw = [s[1:] for s in kw if '-' in s]

        schema = db[store.storeName]
        curr_utc = datetime.utcnow()

        for doc in schema.find({'product_updated_at': {'$lt': curr_utc, '$gte': curr_utc - timedelta(hours=1)}},
                               {'handle': 1, 'title': 1, 'id': 1, 'updated_at': 1, 'variants.id': 1,
                                'variants.price': 1,
                                'variants.available': 1, 'variants.title': 1, 'images.src': 1, 'product_updated_at': 1}
                               ).sort('product_updated_at', pymongo.DESCENDING):

            logger.info(" Product {0} Updated at √ {1}" .format(doc['title'],doc['updated_at']))
            title = doc["title"].lower()
            if all([p in title for p in pkw]) and all([n not in title for n in nkw]):
                try:
                    print('reached keyword')
                    payload = store.json_embed(doc)
                    result = discord_push(webhook_url, payload)
                except IndexError:
                    print('discord embed error')

        logger.info("Listener resting...")
