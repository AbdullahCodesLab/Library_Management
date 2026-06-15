"""add phone number to users

Revision ID: 0733fc8a6281
Revises:
Create Date: 2026-06-15 19:28:36.879760

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0733fc8a6281'

down_revision: Union[str, Sequence[str], None] = None

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        'books',
        'is_issued',
        existing_type=sa.BOOLEAN(),
        nullable=False
    )

    op.alter_column(
        'issued_books',
        'issued_time',
        existing_type=postgresql.TIMESTAMP(),
        nullable=False
    )

    op.add_column(
        'users',
        sa.Column(
            'phone_number',
            sa.String(),
            nullable=True
        )
    )

    op.create_unique_constraint(
        None,
        'users',
        ['phone_number']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        None,
        'users',
        type_='unique'
    )

    op.drop_column(
        'users',
        'phone_number'
    )

    op.alter_column(
        'issued_books',
        'issued_time',
        existing_type=postgresql.TIMESTAMP(),
        nullable=True
    )

    op.alter_column(
        'books',
        'is_issued',
        existing_type=sa.BOOLEAN(),
        nullable=True
    )