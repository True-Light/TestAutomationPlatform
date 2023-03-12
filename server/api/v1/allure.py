import os
import zipfile

from typing import Any, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile, Form, File, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from core import security
from core.config import settings
from core.logger import logger_server
from db.sql_pool import Connection
from crud import crud_allure
from schemas import schema_allure
from utils.allure_backend_task import delete_overdue_files, extract_report, extract_and_generate_report
from api.deps import get_db, get_uuid, connect_db

allure = APIRouter()


@allure.post("/generate-report-from-zip")
@logger_server.catch
async def generate_report_from_zip(
        data: schema_allure.CreateAllureReport,
        background_tasks: BackgroundTasks,
        db: Connection = Depends(get_db),
):
    """
    处理上传的结果
    :param data:
    :param background_tasks:
    :param  db
    :return:
    """
    if data.file[0]['response']['success']:
        file_uuid = data.file[0]['response']['uuid']
    else:
        return {
            "success": False,
            "message": f"未查询到上传的zip文件,请检查是否上传成功!"
        }
    zip_path = os.path.join(settings.UPLOAD_FILES_DIR, f"{file_uuid}.zip")
    extract_path = os.path.join(settings.ALLURE_RESULTS_DIR, file_uuid)
    generate_path = os.path.join(settings.ALLURE_REPORTS_DIR, file_uuid)
    if zipfile.is_zipfile(zip_path):
        try:
            with zipfile.ZipFile(zip_path) as zp:
                zp.testzip()
        except Exception as e:
            return {
                "success": False,
                "message": f"Check zip file error: {e}"
            }
    else:
        return {
            "success": False,
            "message": f"Must be zip file!"
        }
    create_params = schema_allure.CreateParams()
    create_params.zip_path = zip_path
    create_params.extract_path = extract_path
    create_params.generate_path = generate_path
    create_params.uuid = file_uuid
    create_params.job = data.job
    create_params.suite = data.suite
    create_params.feature = data.feature
    create_params.version = data.version
    crud_allure.insert_report_info(db, data=create_params)
    background_tasks.add_task(extract_and_generate_report, create_params)
    return {
        "success": True,
        "data": {"uuid": file_uuid},
    }


@allure.post("/upload-report")
@logger_server.catch
async def create_uploaded_report(
        data: schema_allure.CreateAllureReport,
        background_tasks: BackgroundTasks,
        db: Connection = Depends(get_db),
):
    """
    接受本地上传的allure报告压缩件
    :param data:
    :param background_tasks:
    :param db:
    :return:
    """
    if data.file[0]['response']['success']:
        file_uuid = data.file[0]['response']['uuid']
    else:
        return {
            "success": False,
            "message": f"未查询到上传的zip文件,请检查是否上传成功!"
        }
    zip_path = os.path.join(settings.UPLOAD_FILES_DIR, f"{file_uuid}.zip")
    extract_path = os.path.join(settings.ALLURE_RESULTS_DIR, file_uuid)
    generate_path = os.path.join(settings.ALLURE_REPORTS_DIR, file_uuid)
    create_params = schema_allure.CreateParams()
    create_params.uuid = file_uuid
    create_params.job = data.job
    create_params.suite = data.suite
    create_params.feature = data.feature
    create_params.version = data.version
    create_params.zip_path = zip_path
    create_params.extract_path = extract_path
    create_params.generate_path = generate_path
    crud_allure.create_allure_report(db, data=create_params)
    background_tasks.add_task(extract_report, create_params)
    return {
        "success": True,
        "data": {
            "uuid": file_uuid,
        }
    }


@allure.post("/report-list")
@logger_server.catch
async def query_report_list(
        data: schema_allure.SearchAllureReport,
        db: Connection = Depends(get_db),
):
    current = data.current
    if current < 1:
        return {
            "success": False,
            "message": "错误的页码!"
        }
    page_size = data.pageSize
    fitter_data = {}
    if data.job and data.job != "":
        fitter_data['job'] = data.job
    if data.suite and data.suite != "":
        fitter_data['suite'] = data.suite
    if data.feature and data.feature != "":
        fitter_data['feature'] = data.feature
    if data.version and data.version != "":
        fitter_data['version'] = data.version
    result = crud_allure.query_report_list(
        db, fitter_by=fitter_data if fitter_data else None, current=current, page_size=page_size
    )
    return {
        "success": True,
        "data": result,
    }


@allure.post("/result-list")
@logger_server.catch
async def query_result_list():
    return {
        "success": False,
    }


@allure.get("/remove-overdue-files")
@logger_server.catch
async def remove_overdue_files(
        limitDays: int,
        background_task: BackgroundTasks,
):
    background_task.add_task(delete_overdue_files, limitDays)
    return {
        "success": True,
        "message": "任务已提交,等待服务器处理..."
    }
