"""add_role_to_users

Revision ID: 669aa01ad572
Revises: ed0ab1a1cfee
Create Date: 2026-06-18 20:59:13.704341

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = '669aa01ad572'

down_revision: Union[str, Sequence[str], None] = 'ed0ab1a1cfee'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        'users',

        sa.Column(
            'role',

            sa.String(),

            nullable=True
        )
    )

    op.execute(
        """
        UPDATE users
        SET role='member'
        WHERE role IS NULL
        """
    )

    op.alter_column(
        'users',

        'role',

        nullable=False
    )


def downgrade() -> None:

    op.drop_column(
        'users',

        'role'
    )