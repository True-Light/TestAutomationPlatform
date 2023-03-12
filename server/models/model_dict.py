from sqlalchemy import Column, String, Boolean

from db.base_class import Base


class ComDict(Base):
    __tablename__ = "com_dict"
    data_code = Column(String, nullable=False)
    data_type = Column(String, nullable=False)
    dict_code = Column(String, nullable=False)
    dict_name = Column(String, nullable=False)
    dict_value = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
