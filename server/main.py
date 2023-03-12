# !/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/10/18 23:57
# @Author  : ZhangXin
# @Version : python3.10
# @Modification  :

import time

import uvicorn

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from api.v1.allure import allure
from api.v1.user import user
from api.v1.system import system
from core.config import settings
from core.logger import logger_server

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    logger_server.info(f"TA 获取的请求值为 {dict(request)}")
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(allure, prefix=f"{settings.API_V1_STR}/allure", tags=["allure模块"])
app.include_router(user, prefix=f"{settings.API_V1_STR}/user", tags=["用户模块"])
app.include_router(system, prefix=f"{settings.API_V1_STR}/system", tags=["系统模块"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, workers=1, log_level="debug", reload=True)

"""
celery -A proj worker --loglevel=INFO --concurrency=10 -n worker1@%h
$ celery multi start 1 -A proj -l INFO -c4 --pidfile=/var/run/celery/%n.pid --logfile="$HOME/log/celery/%n%I.log"
$ celery multi restart 1 --pidfile=/var/run/celery/%n.pid
celery -A proj worker -l INFO -Q foo,bar,baz

celery multi stopwait worker1 --pidfile="$HOME/run/celery/%n.pid"

celery -A proj beat

"""
