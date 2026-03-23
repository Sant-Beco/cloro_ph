"""create sites and measurements

Revision ID: 20260323_0001
Revises:
Create Date: 2026-03-23
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260323_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("kind", sa.String(length=50), nullable=False),
        sa.Column("location", sa.String(length=120), nullable=True),
    )
    op.create_index("ix_sites_id", "sites", ["id"])

    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("sampled_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("ph_value", sa.Float(), nullable=False),
        sa.Column("chlorine_value", sa.Float(), nullable=False),
        sa.Column("area", sa.String(length=120), nullable=True),
        sa.Column("observation", sa.Text(), nullable=True),
    )
    op.create_index("ix_measurements_id", "measurements", ["id"])
    op.create_index("ix_measurements_site_id", "measurements", ["site_id"])
    op.create_index("ix_measurements_sampled_at", "measurements", ["sampled_at"])


def downgrade() -> None:
    op.drop_index("ix_measurements_sampled_at", table_name="measurements")
    op.drop_index("ix_measurements_site_id", table_name="measurements")
    op.drop_index("ix_measurements_id", table_name="measurements")
    op.drop_table("measurements")

    op.drop_index("ix_sites_id", table_name="sites")
    op.drop_table("sites")
