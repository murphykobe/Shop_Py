#!/usr/bin/env python
# coding=utf-8

import time
import schedule
import concurrent.futures
from .config import CRAWLER_RUN_CYCLE, LISTENER_RUN_CYCLE
from .crawler import crawler
from .listener import listener
from .logger import logger

def run_schedule(task):
    """
    启动客户端
    """
    # 启动收集器
    schedule.every(CRAWLER_RUN_CYCLE).minutes.do(crawler.run, task.store).run()
    # 启动验证器
    schedule.every(LISTENER_RUN_CYCLE).minutes.do(listener.listener_run, task).run()

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("You have canceled all jobs")
            return
