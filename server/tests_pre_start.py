# !/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/10/18 23:57
# @Author  : ZhangXin
# @Version : python3.10
# @Modification  :
import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlalchemy import text

from db.session import connect_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
max_tries = 60 * 5  # 5 minutes
wait_seconds = 10


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, 20),
    after=after_log(logger, 30),
)
def init() -> None:
    with connect_db() as db:
        db.execute(text("SELECT 1"))


def main() -> None:
    logger.info("TA Initializing service")
    init()
    logger.info("TA Service finished initializing")


if __name__ == "__main__":
    main()
