import datetime

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(Base):
    __tablename__ = 'user'
    username = Column(String(32), unique=True)
    real_name = Column(String(32), index=True, nullable=True)
    email = Column(String(64), unique=True, index=True)
    phone_number = Column(String(32), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class Role(Base):
    __tablename__ = 'role'
    role_name = Column(String(32), unique=True, index=True, nullable=False)


class UserRole(Base):
    __tablename__ = 'user_role'
    user_id = Column(BigInteger, nullable=False)
    role_id = Column(Integer, nullable=False)


class Department(Base):
    __tablename__ = 'department'
    department_name = Column(String(32), unique=True, index=True, nullable=False)
    department_code = Column(String(16))


class DepartmentWithUser(Base):
    __tablename__ = 'department_with_user'
    department_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)


class DepartmentWithRole(Base):
    __tablename__ = "department_with_role"
    department_id = Column(BigInteger, nullable=False)
    role_id = Column(Integer, nullable=False)


class UserGroup(Base):
    __tablename__ = 'user_group'
    user_group_name = Column(String(32), unique=True, index=True)


class UserGroupWithUser(Base):
    __tablename__ = 'user_group_with_user'
    user_group_id = Column(BigInteger, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)


class UserGroupWithRole(Base):
    __tablename__ = 'user_group_with_role'
    user_group_id = Column(BigInteger, nullable=False, index=True)
    role_id = Column(Integer, nullable=False, index=True)


class Menu(Base):
    __tablename__ = 'menu'
    menu_name = Column(String(32), unique=True, index=True)
    menu_url = Column(String(128))
    parent_id = Column(Integer)


class Worker(Base):
    __tablename__ = 'worker'
    worker_id = Column(Integer, nullable=False, index=True)
    worker_name = Column(String(32), unique=True, index=True)
    worker_host = Column(String(64))
    worker_owner = Column(String(32))


class TestCase(Base):
    __tablename__ = 'test_case'
    case_id = Column(String(32))
    case_name = Column(String(32))


class Access(Base):
    __tablename__ = 'access'
    access_name = Column(String(32), unique=True, index=True)
    access_code = Column(String(16))
    access_description = Column(String(128))


class AccessWithMenu(Base):
    __tablename__ = 'access_with_menu'
    access_id = Column(Integer)
    menu_id = Column(Integer)


class AccessWithPage(Base):
    __tablename__ = 'access_with_page'
    access_id = Column(Integer)
    page_id = Column(Integer)


class AccessWithTestCase(Base):
    __tablename__ = 'access_with_test_case'
    access_id = Column(Integer)
    case_id = Column(Integer)


class AccessWithWorker(Base):
    __tablename__ = 'access_with_worker'
    access_id = Column(Integer)
    worker_id = Column(Integer)


class RoleWithAccess(Base):
    __tablename__ = 'user_with_access'
    role_id = Column(Integer)
    access_id = Column(Integer)


class OperationLog(Base):
    __tablename__ = 'operation_log'
    operation_content = Column(String(32))
    operation_user_id = Column(BigInteger)
