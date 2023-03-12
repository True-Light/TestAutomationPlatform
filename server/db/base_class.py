from sqlalchemy.orm import as_declarative
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, DateTime, func, BigInteger


@as_declarative()
class Base:
    __tablename__: str
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
