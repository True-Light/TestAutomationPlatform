from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, text, label

from core.logger import logger_server
from crud.base import CRUDBase
from schemas.schema_allure import CreateAllureReport, UploadAllureReport, CreateParams
from models import Allure


class CRUDAllure(CRUDBase[Allure]):
    def insert_report_info(self, db: Session, *, data: CreateParams):
        params = {
            'uuid': data.uuid,
            'job': data.job,
            'suite': data.suite,
            'feature': data.feature,
            'version': data.version
        }
        self.insert(db, params=params)

    def query_report_list(
            self,
            db: Session,
            *,
            fitter_by: dict | None,
            current: int,
            page_size: int,
    ):
        stmt = select(
            self.model.id, self.model.uuid, self.model.job,
            self.model.suite, self.model.feature,
            self.model.version, self.model.size, self.model.is_generated.label('status'),
            self.model.created_at.label('createTime')
        )
        if fitter_by:
            for key in fitter_by.keys():
                stmt = stmt.where(eval(f"self.model.{key}") == fitter_by[key])
        stmt = stmt.order_by(
            self.model.id.desc()
        ).offset((current - 1) * page_size).limit(page_size)
        result = db.execute(stmt).mappings().all()
        logger_server.debug(f"查询所有报告: {result}")
        return result

    def query_latest_report(self, db: Session, feature):
        stmt = "SELECT id, uuid " \
               "FROM allure t1 " \
               "INNER JOIN " \
               "(SELECT suite, job, version, MAX(id) as `max_id` " \
               "FROM allure " \
               "WHERE is_generated=1 " \
               "GROUP BY  suite, job, version) t2 " \
               "ON t1.suite=t2.suite " \
               "AND t1.job=t2.job " \
               "AND t1.version=t2.version " \
               "WHERE t1.id=t2.max_id AND t1.feature=:feature;"
        result = db.execute(text(stmt), {'feature': feature}).first()
        logger_server.debug(f"查询最新的一条报告: {result}")
        return result

    def query_overdue_report_list(self, db: Session, datetime):
        stmt = select(
            self.model.id, self.model.uuid, self.model.report_path, self.model.is_generated
        ).where(self.model.created_at < datetime)
        result = db.execute(stmt).mappings().all()
        logger_server.debug(f"查询过期报告列表: {result}")
        return result

    def update_report_generated_stats(self, db: Session, uuid, report_path, size):
        stmt = update(self.model).where(
            self.model.uuid == uuid,
        ).values(is_generated=True, report_path=report_path, size=size)
        db.execute(stmt)
        db.commit()


crud_allure = CRUDAllure(Allure)
