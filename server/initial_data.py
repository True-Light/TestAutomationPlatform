# !/usr/bin/env python
# -*-coding:utf-8 -*-
# @Time    : 2021/10/18 23:57
# @Author  : ZhangXin
# @Version : python3.10
# @Modification  :
import logging

from sqlalchemy import text

from db.session import SessionLocal
from crud.crud_user import crud_user
from core.config import settings
from core.security import get_password_hash
from models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    create_list = [
        "CREATE TABLE `user` ("
        "`id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键', "
        "`username` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '账号', "
        "`hashed_password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码', "
        "`real_name` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '姓名', "
        "`email` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱', "
        "`phone` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '电话', "
        "`is_active` tinyint(1) DEFAULT 0 COMMENT '是否激活', "
        "`is_superuser` tinyint(1) DEFAULT 0 COMMENT '超级用户',"
        "`created_at` datetime DEFAULT CURRENT_TIMESTAMP, "
        "`updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP, "
        "PRIMARY KEY (`id`), "
        "UNIQUE KEY `ix_user_username` (`username`), "
        "KEY `ix_user_id` (`id`) "
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;",
        "CREATE TABLE `allure` ( "
        "`id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键', "
        "`uuid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '编码', "
        "`job` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称', "
        "`feature` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '功能名称', "
        "`suite` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '集合名称', "
        "`version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '版本号', "
        "`report_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '报告保存路径', "
        "`is_generated` tinyint NOT NULL DEFAULT '0' COMMENT '报告生成状态', "
        "`size` int DEFAULT '0' COMMENT '磁盘占用', "
        "`level` int DEFAULT '0' COMMENT '等级', "
        "`created_at` datetime DEFAULT CURRENT_TIMESTAMP, "
        "`updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP ,"
        "PRIMARY KEY (`id`), "
        "UNIQUE KEY `ix_allure_uuid` (`uuid`), "
        "KEY `ix_allure_id` (`id` DESC), "
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;",
        "CREATE TABLE `com_dict` ( "
        "`id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键', "
        "`data_code` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据编码', "
        "`data_type` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据类型', "
        "`dict_code` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '字典编码', "
        "`dict_name` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '字典名称', "
        "`dict_value` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '字典值', "
        "`is_active` tinyint DEFAULT '1' COMMENT '是否激活', "
        "`created_at` datetime DEFAULT CURRENT_TIMESTAMP, "
        "`updated_at` datetime DEFAULT NULL  ON UPDATE CURRENT_TIMESTAMP, "
        "PRIMARY KEY (`id`) "
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"
    ]
    for item in create_list:
        try:
            db.execute(text(item))
            db.commit()
        except Exception as e:
            logger.warning(f"Failed to create tables {e}")
    user = crud_user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = User(
            username=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            real_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            is_superuser=True,
            is_active=True,
        )
        db.add(user_in)
        db.commit()


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
