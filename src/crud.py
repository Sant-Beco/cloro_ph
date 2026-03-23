from datetime import datetime
from typing import Optional

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from .models import Measurement, Site
from .schemas import MeasurementCreate


def list_sites(db: Session) -> list[Site]:
    stmt: Select[tuple[Site]] = select(Site).order_by(Site.name.asc())
    return list(db.scalars(stmt).all())


def create_measurement(db: Session, payload: MeasurementCreate) -> Measurement:
    item = Measurement(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_measurements(
    db: Session,
    site_id: Optional[int] = None,
    start_at: Optional[datetime] = None,
    end_at: Optional[datetime] = None,
) -> list[Measurement]:
    stmt: Select[tuple[Measurement]] = select(Measurement).order_by(Measurement.sampled_at.desc())

    if site_id is not None:
        stmt = stmt.where(Measurement.site_id == site_id)
    if start_at is not None:
        stmt = stmt.where(Measurement.sampled_at >= start_at)
    if end_at is not None:
        stmt = stmt.where(Measurement.sampled_at <= end_at)

    return list(db.scalars(stmt).all())
