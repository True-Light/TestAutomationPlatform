from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, text, label

from core.logger import logger_server
from crud.base import CRUDBase
from models import ComDict


class CRUDComDict(CRUDBase[ComDict]):
    def query_enum_list(self, db: Session, data_code: str):
        stmt = select(
            self.model.dict_name.label('label'), self.model.dict_value.label('value')
        ).where(self.model.data_code == data_code, self.model.is_active == True)
        result = db.execute(stmt).mappings().all()
        return result


crud_com_dict = CRUDComDict(ComDict)
