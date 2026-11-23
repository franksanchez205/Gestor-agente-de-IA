"""initial

Revision ID: 514897b2915c
Revises: 
Create Date: 2026-11-22 21:27:33.057273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '514897b2915c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("nationality", sa.String(), nullable=False),
        sa.Column("preferred_language", sa.String(), nullable=True, server_default="es"),
        sa.Column("preferred_channel", sa.String(), nullable=True, server_default="whatsapp"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "documents",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("doc_type", sa.String(), nullable=False),
        sa.Column("issued_by", sa.String(), nullable=False),
        sa.Column("issued_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("credential", sa.JSON(), nullable=True),
    )
    op.create_table(
        "cases",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("tramite", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=True, server_default="pending"),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("gestor_id", sa.String(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("cases")
    op.drop_table("documents")
    op.drop_table("users")