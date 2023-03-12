import datetime

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from core.config import settings
from crud.base import CRUDBase
from models.roles import Roles
from schemas.roles import RolesCreate, RolesUpdate


class CRUDRoles(CRUDBase[Roles]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[Roles]:
        return db.query(self.model).filter(Roles.id == id).first()

    def get_by_role_name(self, db: Session, *, role_name: str) -> Optional[Roles]:
        return db.query(self.model).filter(Roles.roleName == role_name).first()

    def get_server_list(self, db: Session, *, current, page_size, role_id, role_name):
        if role_id and role_name:
            res = db.query(self.model).filter_by(
                roleId=role_id, roleName=role_name
            ).offset((current - 1) * page_size).limit(page_size).all()
        elif (role_id is None) and role_name:
            res = db.query(self.model).filter_by(
                roleName=role_name
            ).offset((current - 1) * page_size).limit(page_size).all()
        elif role_id and (role_name is None):
            res = db.query(self.model).filter_by(
                roleId=role_id
            ).offset((current - 1) * page_size).limit(page_size).all()
        else:
            res = self.get_multi_by_pager(db, current=current, page_size=page_size)
        return res

    def create(self, db: Session, *, obj_in: RolesCreate) -> Roles:
        db_obj = Roles(
            roleId=obj_in.roleId,
            roleName=obj_in.roleName,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Roles, obj_in: Union[RolesUpdate, Dict[str, Any]]
    ) -> Roles:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["updateTime"] = datetime.datetime.now()
        return super().update(db, db_obj=db_obj, obj_in=update_data)


roles = CRUDRoles(Roles)
