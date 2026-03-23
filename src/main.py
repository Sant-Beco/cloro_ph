from datetime import datetime
from typing import Optional

import sentry_sdk
from fastapi import Depends, FastAPI, HTTPException, Query, status
from loguru import logger
from sqlalchemy import text
from sqlalchemy.orm import Session

from . import crud
from .config import settings
from .database import get_db
from .schemas import MeasurementCreate, MeasurementOut, SiteOut

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.1)

logger.remove()
logger.add(lambda message: print(message, end=""), level=settings.log_level)

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/health")
def healthcheck(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/sites", response_model=list[SiteOut])
def get_sites(db: Session = Depends(get_db)) -> list[SiteOut]:
    return crud.list_sites(db)


@app.post("/measurements", response_model=MeasurementOut, status_code=status.HTTP_201_CREATED)
def create_measurement(payload: MeasurementCreate, db: Session = Depends(get_db)) -> MeasurementOut:
    site_exists = any(site.id == payload.site_id for site in crud.list_sites(db))
    if not site_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe la sede con id={payload.site_id}",
        )

    created = crud.create_measurement(db, payload)
    logger.info(
        "Measurement created site_id={} sampled_at={} ph={} cl={}",
        created.site_id,
        created.sampled_at.isoformat(),
        created.ph_value,
        created.chlorine_value,
    )
    return created


@app.get("/measurements", response_model=list[MeasurementOut])
def get_measurements(
    site_id: Optional[int] = Query(default=None),
    start_at: Optional[datetime] = Query(default=None),
    end_at: Optional[datetime] = Query(default=None),
    db: Session = Depends(get_db),
) -> list[MeasurementOut]:
    return crud.list_measurements(db, site_id=site_id, start_at=start_at, end_at=end_at)
