import os
import zipfile

import schemas

from datetime import timedelta
from typing import Any, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile, Form, File
from fastapi.security import OAuth2PasswordRequestForm

from core import security
from core.config import settings
from core.logger import logger_server
from db.sql_pool import Connection
from crud import crud_com_dict
from schemas import schema_allure

from api.deps import get_db, get_uuid

system = APIRouter()


@system.get("/enum-job-list")
async def get_job_list(db: Connection = Depends(get_db)):
    result = crud_com_dict.query_enum_list(db, "000001")
    return {
        "success": True,
        "data": result,
    }


@system.get("/enum-suite-list")
async def get_suite_list(db: Connection = Depends(get_db)):
    result = crud_com_dict.query_enum_list(db, "000002")
    return {
        "success": True,
        "data": result,
    }


@system.get("/enum-feature-list")
async def get_feature_list(db: Connection = Depends(get_db)):
    result = crud_com_dict.query_enum_list(db, "000003")
    return {
        "success": True,
        "data": result,
    }


@system.get("/enum-version-list")
async def get_version_list(db: Connection = Depends(get_db)):
    result = crud_com_dict.query_enum_list(db, "000004")
    return {
        "success": True,
        "data": result,
    }


@system.get("/get-upload-url")
async def get_upload_url(setUrl: str = None):
    if setUrl:
        settings.UPLOAD_ZIP_SERVER = setUrl
    return {
        "success": True,
        "url": settings.UPLOAD_ZIP_SERVER
    }


@system.post("/upload-zip-file")
async def create_upload_report(files: UploadFile = File(...)):
    """
    保存上传的zip文件
    :param files:
    :return:
    """
    file_uuid = get_uuid()
    file_content = await files.read()
    filetype = files.content_type
    if 'zip' not in filetype:
        return {'success': False, 'message': "必须是zip格式的文件!"}
    save_path = os.path.join(settings.UPLOAD_FILES_DIR, f"{file_uuid}.zip")
    with open(save_path, "wb") as fp:
        fp.write(file_content)
    return {
        "success": True,
        "uuid": file_uuid,
    }


@system.get("/healthy")
async def check_healthy():
    return {
        "success": True,
        "code": 0,
    }
