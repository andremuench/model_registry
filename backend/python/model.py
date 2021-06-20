from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from meta import ModelRelease
from typing import Optional, List
import os

ARTIFACT_DEFAULT_BASE_PATH = os.environ.get("ARTIFACT_BASE_PATH", "/models").rstrip("/")

class ModelVersion(BaseModel):
    version: str

class ModelId(BaseModel):
    model_id: str

class ModelInput(ModelVersion, ModelId):
    artifact_path: Optional[str] 

    @property
    def safe_artifact_path(self):
        return self.artifact_path or f"{ARTIFACT_DEFAULT_BASE_PATH}/{self.model_id}/{self.version}/artifacts"

    def to_orm(self) -> ModelRelease:
        return ModelRelease(model_id=self.model_id, version=self.version, artifact_path=self.safe_artifact_path)

ModelReleaseSchema = sqlalchemy_to_pydantic(ModelRelease)

