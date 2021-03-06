"""added created_at column

Revision ID: 889577f95b89
Revises: e757251cad45
Create Date: 2022-05-29 13:46:08.231887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '889577f95b89'
down_revision = 'e757251cad45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('Venue', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'created_at')
    op.drop_column('Artist', 'created_at')
    # ### end Alembic commands ###
