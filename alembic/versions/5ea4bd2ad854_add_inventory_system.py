"""add_inventory_system

Revision ID: 5ea4bd2ad854
Revises: 669aa01ad572
Create Date: 2026-06-18 22:44:23.751807

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5ea4bd2ad854'

down_revision: Union[str, Sequence[str], None] = '669aa01ad572'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(

        'books',

        sa.Column(

            'total_copies',

            sa.Integer(),

            nullable=False,

            server_default='1'
        )
    )

    op.add_column(

        'books',

        sa.Column(

            'available_copies',

            sa.Integer(),

            nullable=False,

            server_default='1'
        )
    )

    op.drop_column(

        'books',

        'is_issued'
    )


def downgrade() -> None:

    op.add_column(

        'books',

        sa.Column(

            'is_issued',

            sa.Boolean(),

            nullable=False,

            server_default='false'
        )
    )

    op.drop_column(

        'books',

        'available_copies'
    )

    op.drop_column(

        'books',

        'total_copies'
    )