import datetime

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from core.config import settings
from core.security import get_password_hash, verify_password, decrypt_data
from crud.base import CRUDBase
from models.user import User
from crud.crue_roles import roles
from schemas.user import UserCreate, UserUpdate, UserLogin, UserUpdatePassword


class CRUDUser(CRUDBase[User]):

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(self.model).filter(User.username == username).first()

    def get_user_list(self, db: Session, *, current, page_size, username, full_name):
        if username and full_name:
            res = db.query(self.model).filter_by(
                username=username, fullName=full_name
            ).offset((current - 1) * page_size).limit(page_size).all()
        elif (username is None) and full_name:
            res = db.query(self.model).filter_by(
                fullName=full_name
            ).offset((current - 1) * page_size).limit(page_size).all()
        elif username and (full_name is None):
            res = db.query(self.model).filter_by(
                username=username
            ).offset((current - 1) * page_size).limit(page_size).all()
        else:
            res = self.get_multi(db, current=current, page_size=page_size)
        return res

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # 特殊情况,前端回传的实际是 roles表的id 或者 roleName
        try:
            c_id = int(obj_in.roleName)
            get_roles = roles.get_by_id(db, id=c_id)
        except:  # noqa
            get_roles = roles.get_by_role_name(db, role_name=obj_in.roleName)
        username = decrypt_data(obj_in.username)
        password = decrypt_data(obj_in.password)
        obj_in.username = username
        obj_in.password = password
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            hashedPassword=get_password_hash(obj_in.password),
            fullName=obj_in.fullName,
            isSuperuser=False,
            isActive=False,
            roleCode=get_roles.roleCode,
            roleName=get_roles.roleName,
            createTime=datetime.datetime.now(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        # 特殊情况,前端回传的实际是 roles表的id 或者 roleName
        try:
            c_id = int(obj_in.roleName)
            get_roles = roles.get_by_id(db, id=c_id)
        except:  # noqa
            get_roles = roles.get_by_role_name(db, role_name=obj_in.roleName)
        username = decrypt_data(obj_in.username)
        password = decrypt_data(obj_in.password)
        obj_in.username = username
        obj_in.password = password
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashedPassword"] = hashed_password
        update_data["roleName"] = get_roles.roleName
        update_data["roleCode"] = get_roles.roleCode
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def update_password(self, db, *, id: int, hashed_password: str, data: UserUpdatePassword):
        old_password = decrypt_data(data.passwordOld)
        new_password = decrypt_data(data.passwordNew)
        if verify_password(old_password, hashed_password):
            db.query(self.model).filter(User.id == id).update({"hashedPassword": get_password_hash(new_password)})
            db.commit()
            return True
        else:
            return False

    def is_user_exits(self, db: Session):
        return

    def set_user_active(self, db: Session, *, id, is_active):
        db.query(self.model).filter(User.id == id).update({"isActive": is_active})
        db.commit()
        return

    def set_user_superuser(self, db: Session, *, id, is_superuser):
        db.query(self.model).filter(User.id == id).update({"isSuperuser": is_superuser})
        db.commit()
        return

    def authenticate_test(self, db: Session, *, username: str, password: str):
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashedPassword):
            return None
        return user

    def authenticate(self, db: Session, *, login_data: UserLogin) -> Union[User, int]:
        username = decrypt_data(login_data.username)
        password = decrypt_data(login_data.password)
        if not username or not password:
            return 1000
        this_user = self.get_by_username(db, username=username)
        if not this_user:
            return 1001
        if not verify_password(password, this_user.hashedPassword):
            return 1002
        if not self.is_active(this_user):
            return 1003
        return this_user

    def is_active(self, user: User) -> bool:
        return user.isActive

    def is_superuser(self, user: User) -> bool:
        return user.isSuperuser


crud_user = CRUDUser(User)
