"""add_waitlist_table

Revision ID: 2a7b35ab1906
Revises: 5ea4bd2ad854
Create Date: 2026-06-18 23:27:38.435448

"""

from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


revision: str = "2a7b35ab1906"

down_revision: Union[str, Sequence[str], None] = "5ea4bd2ad854"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(

        "waitlists",

        sa.Column(

            "id",

            sa.Integer(),

            nullable=False
        ),

        sa.Column(

            "user_id",

            sa.Integer(),

            nullable=False
        ),

        sa.Column(

            "book_id",

            sa.Integer(),

            nullable=False
        ),

        sa.Column(

            "created_at",

            sa.DateTime(),

            nullable=False
        ),

        sa.ForeignKeyConstraint(

            ["user_id"],

            ["users.id"]
        ),

        sa.ForeignKeyConstraint(

            ["book_id"],

            ["books.id"]
        ),

        sa.PrimaryKeyConstraint(
            "id"
        )
    )

    op.create_index(

        "ix_waitlists_id",

        "waitlists",

        ["id"],

        unique=False
    )


def downgrade() -> None:

    op.drop_index(

        "ix_waitlists_id",

        table_name="waitlists"
    )

    op.drop_table(
        "waitlists"
    )