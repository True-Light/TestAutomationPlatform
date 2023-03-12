import os

from loguru import logger
from core.config import settings

# logger.add(
#     sink=os.path.join(settings.LOG_DIR, 'db_{time}.log'),
#     filter=lambda record: record['extra']['name'] == 'db',
#     format="{time} - {level} - {message}",
#     level=settings.LOGURU_LEVEL,
#     rotation='2 MB',
#     enqueue=True,
#     encoding='utf-8',
#     backtrace=True,
#     diagnose=True,
#     colorize=True,
# )

logger.add(
    sink=os.path.join(settings.LOG_DIR, 'server_record.log'),
    filter=lambda record: record['extra']['name'] == 'server',
    format="{time} - {level} - {message}",
    level=settings.LOGURU_LEVEL,
    rotation='5 MB',
    compression='zip',
    enqueue=True,
    encoding='utf-8',
    backtrace=True,
    diagnose=True,
    colorize=True,
)

logger.add(
    sink=os.path.join(settings.LOG_DIR, 'celery_record.log'),
    filter=lambda record: record['extra']['name'] == 'celery',
    format="{time} - {level} - {message}",
    level=settings.LOGURU_LEVEL,
    rotation='5 MB',
    compression='zip',
    enqueue=True,
    encoding='utf-8',
    backtrace=True,
    diagnose=True,
    colorize=True,
)

# logger_db = logger.bind(name="db")
logger_server = logger.bind(name='server')
logger_celery = logger.bind(name='celery')
