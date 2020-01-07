#!/usr/bin/env python
# coding=utf-8

import time
from datetime import datetime

import pymongo

from .config import DBNAME, MONGODB_HOST, MONGODB_PORT
from .logger import logger
from .utils import requests

all_funcs = []
conn = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = conn[DBNAME]

def collect_funcs(func):
    """
    装饰器，用于收集爬虫函数
    """
    all_funcs.append(func)
    return func

class Crawler:

    @staticmethod
    def run(store):
        """
        启动收集器
        """
        logger.info("Crawler working...")
        start_time = time.perf_counter()

        for func in all_funcs:
            schema = db[store.storeName]
            for page in func(store):
                if not page["products"]:
                    break
                for data in page["products"]:
                    data['product_updated_at'] = datetime.strptime(data['updated_at'], '%Y-%m-%dT%H:%M:%S%z')
                    schema.update_one({"id": data["id"]}, {'$set': data}, upsert=True)
                    logger.info(" Product {%s} Update √ {}" % data["title"])

        end_time = time.perf_counter()
        print('Download finished in {} seconds'.format(end_time - start_time))
        logger.info("Crawler resting...")

    @staticmethod
    @collect_funcs
    def crawl_shopify(store):

        request_url = store.json_url
        payload_data = requests(request_url)
        return payload_data

crawler = Crawler()

#request_url = store.json_url
#url_list = list(map(lambda x: request_url + '?limit=250&page=' + str(x), range(1, 36)))
#tasks = [self.]
#pages = await asyncio.gather(*tasks)