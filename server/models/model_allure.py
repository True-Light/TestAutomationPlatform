from sqlalchemy import Column, Integer, String, DateTime, UUID, Boolean

from db.base_class import Base


class Allure(Base):
    __tablename__ = "allure"
    uuid = Column(String, nullable=False)
    job = Column(String, nullable=False)
    feature = Column(String, nullable=False)
    suite = Column(String, nullable=False)
    report_path = Column(String, default=None)
    version = Column(Integer, default=0, nullable=False)
    is_generated = Column(Boolean, default=False)
    size = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=0, nullable=False)
