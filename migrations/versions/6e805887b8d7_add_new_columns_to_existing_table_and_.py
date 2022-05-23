"""add new columns to existing table and create shows table

Revision ID: 6e805887b8d7
Revises: 265928c63a7f
Create Date: 2022-05-22 11:13:49.192683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e805887b8d7'
down_revision = '265928c63a7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.drop_column('Artist', 'seeking_venue')
    op.add_column('Venue', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'past_shows_count')
    op.drop_column('Venue', 'upcoming_shows_count')
    op.add_column('Artist', sa.Column('seeking_venue', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'upcoming_shows_count')
    op.drop_table('Show')
    # ### end Alembic commands ###