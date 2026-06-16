"""add_password_to_users

Revision ID: ed0ab1a1cfee
Revises: 0733fc8a6281
Create Date: 2026-06-16 22:47:16.370290

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ed0ab1a1cfee"

down_revision: Union[str, Sequence[str], None] = "0733fc8a6281"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "users",

        sa.Column(
            "password",

            sa.String(),

            nullable=True
        )
    )

    op.execute(
        """
        UPDATE users
        SET password='temporary_password'
        WHERE password IS NULL
        """
    )

    op.alter_column(
        "users",

        "password",

        nullable=False
    )


def downgrade() -> None:

    op.drop_column(
        "users",

        "password"
    )