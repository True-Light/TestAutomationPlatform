import os
import zipfile
import shutil
import subprocess
import datetime

from core.config import settings
from core.logger import logger_server
from crud import crud_allure
from schemas import schema_allure
from api.deps import connect_db


@logger_server.catch
def delete_overdue_files(days: int):
    latest_zip_date = datetime.datetime.now() - datetime.timedelta(days=7)
    logger_server.info(f"BackendTask 扫描过期的压缩文件 {latest_zip_date}")
    for file in os.listdir(settings.UPLOAD_FILES_DIR):
        this_file = os.path.join(settings.UPLOAD_FILES_DIR, file)
        if ('zip' in file) and os.path.isfile(this_file) and (
                datetime.datetime.fromtimestamp(os.path.getctime(this_file)) < latest_zip_date):  # noqa
            os.remove(this_file)
            logger_server.info(f"删除过期压缩文件 {this_file}")
        else:
            logger_server.info(f"{this_file} {datetime.datetime.fromtimestamp(os.path.getctime(this_file))} 尚未失效")
    # TODO: 调试设置为秒
    latest_date = datetime.datetime.now() - datetime.timedelta(days=days)
    logger_server.info(f"BackendTask 准备查询早于 {latest_date} 的文件")
    with connect_db() as db:
        res = crud_allure.query_overdue_report_list(db, latest_date)
        logger_server.info(f"BackendTask 查询到的过期数据是 {res}")
        for item in res:
            logger_server.info(f'BackendTask 准备删除报告 {item}')
            try:
                if item['report_path'] and os.path.exists(item['report_path']):
                    shutil.rmtree(item['report_path'])
                    logger_server.info(f'BackendTask 删除报告成功 {item["report_path"]}')
                else:
                    logger_server.warning(f'BackendTask 报告路径不存在 {item["report_path"]}, 仅删除数据库')
                crud_allure.delete(db, _id=item['id'])
            except Exception as e:
                logger_server.exception(f'BackendTask 删除报告失败 {item["report_path"]} \n {e}')


@logger_server.catch
def extract_report(data: schema_allure.CreateParams):
    with zipfile.ZipFile(data.zip_path) as zp:
        zp.extractall(data.extract_path)
    logger_server.info(f"BackendTask {data.zip_path}解压完成")
    if len(n := os.listdir(data.extract_path)) == 1:
        logger_server.warning(f"BackendTask 尝试移动不符合条件的文件夹 {n}")
        shutil.move(os.path.join(data.extract_path, n[0]), data.generate_path)
    else:
        shutil.move(data.extract_path, data.generate_path)
    with connect_db() as db:
        size_count = 0
        try:
            for root, dirs, files in os.walk(data.generate_path):
                for f in files:
                    size_count += os.path.getsize(os.path.join(root, f))
            data.size = int(size_count / 1024 / 1024)
        except Exception as e:
            logger_server.exception(f"BackendTask 统计报告容量出错 {e}")
        crud_allure.update_report_generated_stats(db, data.uuid, data.generate_path, data.size)
        logger_server.info(f"BackendTask 处理报告成功! 保存路径为 {data.generate_path}")


@logger_server.catch
def extract_and_generate_report(data: schema_allure.CreateParams):
    result_path = data.extract_path
    with zipfile.ZipFile(data.zip_path) as zp:
        zp.extractall(data.extract_path)
    logger_server.info(f"BackendTask {data.zip_path}解压完成")
    if len(n := os.listdir(data.extract_path)) <= 3:
        logger_server.warning(f"BackendTask 尝试移动不符合条件的文件夹 {n}")
        result_path = os.path.join(data.extract_path, data.uuid)
        shutil.move(os.path.join(data.extract_path, n[0]), result_path)
    # 移动allure 插件配置文件
    shutil.copy(os.path.join(settings.PLUGINS_DIR, 'categories.json'), result_path)
    shutil.copy(os.path.join(settings.PLUGINS_DIR, 'environment.properties'), result_path)
    with connect_db() as db:
        result = crud_allure.query_latest_report(db, data.feature)
        logger_server.info(f"BackendTask 查询最近一条相关报告是{result}")
        if result:
            expect_copy_path = os.path.join(settings.ALLURE_REPORTS_DIR, result[1], 'history')
            if os.path.exists(expect_copy_path):
                shutil.copytree(expect_copy_path, os.path.join(result_path, "history"))
                logger_server.info(f"BackendTask 复制{result[1]}历史数据成功")
                logger_server.debug(f"BackendTask {os.listdir(result_path)}")
            else:
                logger_server.warning(f"BackendTask 历史数据路径不正确: {expect_copy_path}")
        else:
            logger_server.warning(f"BackendTask 未找到符合条件的历史数据")
        logger_server.info("BackendTask 准备生成测试报告")
        proc = subprocess.Popen(
            f"allure generate -c {result_path} -o {data.generate_path}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            outs, errs = proc.communicate(timeout=600)
        except Exception as e:
            proc.kill()
            outs, errs = proc.communicate()
            logger_server.warning(f"BackendTask 执行allure命令的错误信息 {e}")
        logger_server.info(f"BackendTask allure 过程信息 {outs}")
        logger_server.warning(f"BackendTask allure 错误信息 {errs}")
        logger_server.info(f"BackendTask allure 返回值 {proc.returncode}")
        if proc.returncode == 0:
            size_count = 0
            try:
                for root, dirs, files in os.walk(data.generate_path):
                    for f in files:
                        size_count += os.path.getsize(os.path.join(root, f))
                data.size = int(size_count / 1024 / 1024)
            except Exception as e:
                logger_server.exception(f"BackendTask 统计报告容量出错 {e}")
            crud_allure.update_report_generated_stats(db, data.uuid, data.generate_path, data.size)
            logger_server.info(f"BackendTask 执行生成报告成功! 保存路径为 {data.generate_path}")
            logger_server.info(f"BackendTask 开始删除结果文件 {data.extract_path}")
            shutil.rmtree(data.extract_path)
            logger_server.info(f"BackendTask 删除结果成功 {data.extract_path}")
        else:
            logger_server.warning(f"BackendTask 执行生成报告失败! 对应的报告uuid是 {data.uuid}")
