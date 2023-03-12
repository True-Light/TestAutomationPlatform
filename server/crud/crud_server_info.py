import datetime

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from core.config import settings
from core.security import decrypt_data
from crud.base import CRUDBase
from models.server_info import ServerInfo
from schemas.server_info import ServerInfoCreate, ServerInfoUpdate


class CRUDServerInfo(CRUDBase[ServerInfo]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[ServerInfo]:
        return db.query(self.model).filter(ServerInfo.id == id).first()

    def get_server_list(self, db: Session, *, current, page_size, host, server_name):
        if host and server_name:
            res = db.query(self.model).filter_by(
                serverName=server_name, host=host
            ).offset((current - 1) * page_size).limit(page_size).all()
        elif (host is None) and server_name:
            res = db.query(self.model).filter_by(
                serverName=server_name
            ).offset((current - 1) * page_size).limit(page_size).all()
        elif host and (server_name is None):
            res = db.query(self.model).filter_by(
                host=host
            ).offset((current - 1) * page_size).limit(page_size).all()
        else:
            res = self.get_multi_by_pager(db, current=current, page_size=page_size)
        return res

    def create(self, db: Session, *, obj_in: ServerInfoCreate) -> ServerInfo:
        db_obj = ServerInfo(
            host=obj_in.host,
            port=obj_in.port,
            username=obj_in.cUsername,
            password=obj_in.verifyKey + obj_in.cPassword,
            database=obj_in.database,
            serverName=obj_in.serverName,
            createTime=datetime.datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: ServerInfo, obj_in: Union[ServerInfoUpdate, Dict[str, Any]]
    ) -> ServerInfo:
        obj_in.cPassword = obj_in.verifyKey + obj_in.cPassword
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["updateTime"] = datetime.datetime.now()
        return super().update(db, db_obj=db_obj, obj_in=update_data)


server_info = CRUDServerInfo(ServerInfo)
