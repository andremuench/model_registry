from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from meta import ModelRelease, Base
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging
import os


def engine_from_env():
    db_host = os.environ.get("DATABASE_HOST")
    user = os.environ.get("DATABASE_USER")
    pwd = os.environ.get("DATABASE_PASSWD")
    db_name = os.environ.get("DATABASE_NAME")
    db_port = os.environ.get("DATABASE_PORT", 1433)
    return create_engine(f"mssql+pymssql://{user}:{pwd}@{db_host}:{db_port}/{db_name}")


# ---

engine = engine_from_env()
LocalSession = sessionmaker(bind=engine)
logging.basicConfig(level=logging.INFO)


class ModelExistsError(Exception):
    pass


class NotFoundError(Exception):
    pass


class DatabaseStore:
    def __init__(self):
        pass

    def all(self, db: Session):
        return db.query(ModelRelease).all()

    def insert(self, db: Session, release: ModelRelease):
        try:
            db.add(release)
            db.commit()
        except IntegrityError:
            raise ModelExistsError

    def find_unique(self, db: Session, name: str, version: str):
        logging.info(f"Searching model with name {name} and version {version} ")
        return (
            db.query(ModelRelease)
            .filter(ModelRelease.model_id == name)
            .filter(ModelRelease.version == version)
            .first()
        )

    def find(self, db:Session, name: str, version: str=None):
        logging.info(f"Searching model with name: {name} and version: {version}")
        q = db.query(ModelRelease).filter(ModelRelease.model_id == name)
        if version:
            q = q.filter(ModelRelease.version == version)
        return q.all()

    def find_current(self, db: Session, name: str):
        curr = (
            db.query(ModelRelease)
            .filter(ModelRelease.model_id == name)
            .filter(ModelRelease.is_active == True)
            .first()
        )
        if not curr:
            raise NotFoundError
        return curr

    def activate(self, db: Session, model: ModelRelease):
        upd_models = (
            db.query(ModelRelease)
            .filter(
                (
                    (ModelRelease.model_id == model.model_id)
                    & (ModelRelease.version == model.version)
                )
                | (ModelRelease.is_active == True)
            )
            .all()
        )
        if len(upd_models) == 0:
            raise NotFoundError
        _found = False
        for m in upd_models:
            if m.version == model.version:
                m.is_active = 1
                m.go_live_on = datetime.now()
                _found = True
            else:
                m.is_active = 0
        if _found:
            db.commit()
        else:
            db.rollback()
            raise NotFoundError
