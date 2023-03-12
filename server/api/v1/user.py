import schemas

from datetime import timedelta
from typing import Any, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core import security
from core.config import settings
from api.deps import get_db, get_current_user

user = APIRouter()


@user.post("/login/account")
async def login_account(
        login_data: schemas.UserLogin,
        db: Session = Depends(get_db),
) -> Any:
    """
    登录接口
    :param login_data:
    :param  db
    :return:
    """
    # check_res = user.authenticate(db, login_data=login_data)
    check_res = None

    security.decrypt_data(login_data.username)
    security.decrypt_data(login_data.password)

    match check_res:
        case 1000:
            return {
                'code': -1,
                'type': 'error',
                'message': "数据解析错误,请联系开发人员",
                'result': {}
            }
        case 1001:
            return {
                'code': -1,
                'type': 'error',
                'message': "账号不存在",
                'result': {}
            }

        case 1002:
            return {
                'code': -1,
                'type': 'error',
                'message': "账号或密码错误",
                'result': {}
            }
        case 1003:
            return {
                'code': -1,
                'type': 'error',
                'message': "账号未激活",
                'result': {}
            }
        case _:
            # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            return {
                'status': "ok",
                'type': "account",
                "currentAuthority": "token123455"
            }


@user.get("/current-user")
async def get_current_user():
    return {
        "success": True,
        "data": {
            "name": '测试人员',
            "avatar": 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png',
            "userid": '00000001',
            "email": 'tester@tester.com',
            "notify_count": 0,
            "unread_count": 0,
            "country": 'China',
            "access": ["guest"],  # ["admin", "guest"],
            "address": 'beijing',
            "phone": '18888888888',
        },
    }


@user.get("/get-current-menu")
async def get_user_menu(db: Session = Depends(get_db), ) -> Any:
    """
    登录接口
    :param  db
    :return:
    """
    return {
        "success": True,
        "data": [
            {
                'path': '/user',
                'layout': False,
                'routes': [
                    {
                        'name': 'login',
                        'path': '/user/login',
                        'component': './User/Login',
                    },
                ],
            },
            {
                'path': '/welcome',
                'name': 'welcome',
                'icon': 'smile',
                'component': './Welcome',
            },
            {
                'path': '/project',
                'name': 'project',
                'icon': 'folder',
                'routes': [
                    {
                        'path': '/project',
                        'redirect': '/project/pu',
                    },
                    {
                        'name': 'pu',
                        'path': '/project/pu',
                        'component': './Project/Pu',
                    },
                ],
            },
            {
                'path': '/admin',
                'name': 'admin',
                'icon': 'crown',
                'access': 'canAdmin',
                'routes': [
                    {
                        'path': '/admin',
                        'redirect': '/admin/sub-page',
                    },
                    {
                        'path': '/admin/sub-page',
                        'name': 'sub-page',
                        'component': './Admin',
                    },
                ],
            },
            {
                'name': 'list.table-list',
                'icon': 'table',
                'path': '/list',
                'component': './TableList',
            },
            {
                'path': '/',
                'redirect': '/welcome',
            },
            {
                'path': '*',
                'layout': False,
                'component': './404',
            },
        ]
    }


@user.post("/out-login")
async def out_login():
    return {"success": True, "type": "account"}


@user.get("/notices")
async def get_current_user():
    return {
        "data": [
            {
                "id": '000000001',
                "avatar": 'https://gw.alipayobjects.com/zos/rmsportal/ThXAXghbEsBCCSDihZxY.png',
                "title": '你收到了 1 份新周报',
                "datetime": '2022-08-09',
                "type": 'notification',
            }
        ]
    }
