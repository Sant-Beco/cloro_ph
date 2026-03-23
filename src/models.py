from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    kind: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="site", cascade="all, delete-orphan"
    )


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False, index=True)
    sampled_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    ph_value: Mapped[float] = mapped_column(Float, nullable=False)
    chlorine_value: Mapped[float] = mapped_column(Float, nullable=False)
    area: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    observation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    site: Mapped["Site"] = relationship(back_populates="measurements")
