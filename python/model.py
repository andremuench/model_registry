from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from meta import ModelRelease as ModelRelease


class ModelVersion(BaseModel):
    version: str


class ModelInput(ModelVersion):
    model_id: str

    def to_orm(self) -> ModelRelease:
        return ModelRelease(model_id=self.model_id, version=self.version)


ModelReleaseSchema = sqlalchemy_to_pydantic(ModelRelease)