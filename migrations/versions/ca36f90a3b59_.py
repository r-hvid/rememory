"""empty message

Revision ID: ca36f90a3b59
Revises: 894f439c99ac
Create Date: 2018-12-04 20:42:31.030032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca36f90a3b59'
down_revision = '894f439c99ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_queue_queue_entry_point', table_name='queue')
    op.drop_table('queue')
    op.add_column('topics', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('topics', 'body_html')
    op.create_table('queue',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('topic_id', sa.INTEGER(), nullable=False),
    sa.Column('queue_entry_point', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_queue_queue_entry_point', 'queue', ['queue_entry_point'], unique=False)
    # ### end Alembic commands ###
