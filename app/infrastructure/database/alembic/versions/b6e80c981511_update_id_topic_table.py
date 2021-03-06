"""update id Topic table

Revision ID: b6e80c981511
Revises: e63c68d4f25d
Create Date: 2021-11-24 20:42:48.094312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6e80c981511"
down_revision = "e63c68d4f25d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("ix_topics_id"), "topics", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_topics_id"), table_name="topics")
    # ### end Alembic commands ###
