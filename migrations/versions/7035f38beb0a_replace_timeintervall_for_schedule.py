"""Replace TimeIntervall for Schedule

Revision ID: 7035f38beb0a
Revises: 52d47d500ff9
Create Date: 2023-11-05 23:56:23.942272

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7035f38beb0a'
down_revision = '52d47d500ff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('location', sa.String(length=150), nullable=True),
    sa.Column('duty_cycle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['duty_cycle_id'], ['duty_cycle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('time_interval')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_interval',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('start_time', postgresql.TIME(), autoincrement=False, nullable=False),
    sa.Column('end_time', postgresql.TIME(), autoincrement=False, nullable=False),
    sa.Column('load_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['load_id'], ['load.id'], name='time_interval_load_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='time_interval_pkey')
    )
    op.drop_table('schedule')
    # ### end Alembic commands ###