from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SiteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    kind: str
    location: Optional[str]


class MeasurementCreate(BaseModel):
    site_id: int
    sampled_at: datetime
    ph_value: float = Field(ge=0, le=14)
    chlorine_value: float = Field(ge=0)
    area: Optional[str] = None
    observation: Optional[str] = None


class MeasurementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    site_id: int
    sampled_at: datetime
    ph_value: float
    chlorine_value: float
    area: Optional[str]
    observation: Optional[str]
