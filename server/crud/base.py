from typing import Optional, Type, TypeVar, Sequence, Generic

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        :param model A SQLAlchemy model class
        """
        self.model = model

    def get_by_id(self, db: Session, _id: int) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == _id)
        return db.execute(stmt).first()

    def get_first(self, db: Session):
        stmt = select(self.model)
        return db.execute(stmt).first()

    def get_multi(
            self,
            db: Session,
            *,
            current: int,
            page_size: int,
            fitter_by: dict | None = None,
    ):
        if fitter_by:
            stmt = select(self.model).where(**fitter_by).offset((current - 1) * page_size).limit(page_size)
        else:
            stmt = select(self.model).offset((current - 1) * page_size).limit(page_size)
        return db.execute(stmt).scalars().all()

    def insert(self, db: Session, *, params: dict | Sequence[dict]):
        stmt = insert(self.model).values(params)
        db.execute(stmt)
        db.commit()

    def update(self, db: Session, *, params: dict | Sequence[dict]):
        _id = params.pop('id')
        stmt = update(self.model).where(self.model.id == _id).values(params)
        db.execute(stmt)
        db.commit()

    def delete(self, db: Session, *, _id: int):
        stmt = delete(self.model).where(self.model.id == _id)
        db.execute(stmt)
        db.commit()
