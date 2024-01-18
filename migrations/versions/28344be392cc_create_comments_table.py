""" create_comments_table

Revision ID: 28344be392cc
Revises: d4cba328ff70
Create Date: 2024-01-08 19:00:48.988360

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "28344be392cc"
down_revision = "d4cba328ff70"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("text", sa.String(200), nullable=False),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("posts.id")),
    )


def downgrade() -> None:
    op.drop_table("comments")
