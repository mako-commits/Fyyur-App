"""changed boolean column to string

Revision ID: ade1657d4eed
Revises: 4ed474f62701
Create Date: 2022-05-21 19:34:40.333428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ade1657d4eed'
down_revision = '4ed474f62701'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
