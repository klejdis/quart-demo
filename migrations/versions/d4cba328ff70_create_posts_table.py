"""create posts table

Revision ID: d4cba328ff70
Revises:  (empty)
Create Date: 2023-09-22 16:00:30.307438

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d4cba328ff70"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.String(200)),
    )


def downgrade() -> None:
    op.drop_table("posts")
