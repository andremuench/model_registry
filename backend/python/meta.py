from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime, Boolean
from sqlalchemy.sql.expression import null

Base = declarative_base()


class ModelRelease(Base):
    __tablename__ = "tbl_model_release"

    model_id = Column(String(50), primary_key=True)
    version = Column(String(50), primary_key=True)
    artifact_path = Column(String(1000), nullable=True)
    go_live_on = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)
