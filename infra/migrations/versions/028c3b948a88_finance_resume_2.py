"""finance resume 2

Revision ID: 028c3b948a88
Revises: 777865247b26
Create Date: 2024-12-18 14:10:28.641399

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "028c3b948a88"
down_revision: Union[str, None] = "777865247b26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "finance_resumes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("last_month_id", sa.String(), nullable=True),
        sa.Column("recipe", sa.Float(), nullable=True),
        sa.Column("input", sa.Float(), nullable=True),
        sa.Column("output", sa.Float(), nullable=True),
        sa.Column("community_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["community_id"],
            ["communities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["last_month_id"],
            ["finances.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("last_month_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("finance_resumes")
    # ### end Alembic commands ###
