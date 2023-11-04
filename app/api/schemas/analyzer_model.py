from pydantic import BaseModel, Field
import uuid
import datetime as datetime_dt


class ModelReportBase(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    datetime: datetime_dt.datetime
    configuration: dict | list

    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
        from_attributes = True


class ModelReportRead(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    datetime: datetime_dt.datetime
    configuration: dict | list

    class Config:
        orm_mode = True
        from_attributes = True


class ModelReportCreate(BaseModel):
    datetime: datetime_dt.datetime
    configuration: dict | list

    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
        from_attributes = True


class ModelReportUpdate(BaseModel):
    configuration: dict | list

    class Config:
        orm_mode = True
        from_attributes = True


class ModelReportId(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)