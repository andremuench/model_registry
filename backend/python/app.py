from model import ModelInput, ModelReleaseSchema, ModelVersion, ModelId
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from db_store import (
    DatabaseStore,
    ModelExistsError,
    LocalSession,
    engine,
    NotFoundError as DbNotFoundError,
)
import os
import urllib.parse
from meta import ModelRelease, Base
from sqlalchemy.orm import Session
import logging

app = FastAPI(
    title="Model Registry API",
    description="API to provide an interface to manage model metadata",
    version="0.1",
)
db = DatabaseStore()

if os.environ.get("DEV_MODE"):
    from fastapi.middleware.cors import CORSMiddleware
    origins = [
    "http://localhost:8001",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Create Database Structure
logging.info("Create Database structure")
base = Base()
base.metadata.create_all(engine)

logging.info("Test connection")
conn = engine.connect()
conn.close()
# -------


def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


@app.get("/model", responses={200: {"model": ModelReleaseSchema}})
async def get_model_release(
    name: str, version: str, session: Session = Depends(get_db)
):
    m = db.find_unique(session, name=name, version=version)
    if m:
        return m
    raise HTTPException(status_code=404, detail="No such model")

@app.get("/model/find", responses={200: {"model": List[ModelReleaseSchema]}})
async def find_model_release(
    name: str, version: Optional[str]=None, session: Session = Depends(get_db)
):
    models = db.find(session, name=name, version=version)
    if models:
        return [ModelReleaseSchema.from_orm(m) for m in models]
    raise HTTPException(status_code=404, detail="No such model")

@app.get("/model/ids", responses={200: {"model": List[ModelId]}})
async def all_model_ids(
    session: Session = Depends(get_db)
):
    model_ids = db.all_model_ids(session)
    return [ModelId(model_id=m[0]) for m in model_ids]

@app.get("/models", responses={200: {"model": List[ModelReleaseSchema]}})
async def all_model_releases(session: Session = Depends(get_db)):
    return [ModelReleaseSchema.from_orm(m) for m in db.all(session)]


@app.post("/models", status_code=201, responses={302: {}})
async def new_model_release(model: ModelInput, session: Session = Depends(get_db)):
    release = model.to_orm()
    try:
        db.insert(session, release)
    except ModelExistsError:
        raise HTTPException(
            status_code=302,
            detail="Model exists",
            headers={
                "Location": app.url_path_for("get_model_release")
                + "?"
                + urllib.parse.urlencode(
                    {"name": model.model_id, "version": model.version}
                )
            },
        )
    return "ok"


@app.get(
    "/models/{name}/current", responses={200: {"model": ModelReleaseSchema}, 404: {}}
)
async def get_current_model_release(name: str, session: Session = Depends(get_db)):
    try:
        return ModelReleaseSchema.from_orm(db.find_current(session, name))
    except DbNotFoundError:
        raise HTTPException(status_code=404, detail="No current model")


@app.put("/models/{name}/current", status_code=200, responses={404: {}})
async def set_current_model_release(
    name: str, version: ModelVersion, session: Session = Depends(get_db)
):
    try:
        db.activate(session, ModelRelease(model_id=name, version=version.version))
        return "ok"
    except DbNotFoundError:
        raise HTTPException(status_code=404, detail="No such models")
