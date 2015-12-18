"""empty message

Revision ID: 33f4cda3c0bf
Revises: 216b3571df6c
Create Date: 2015-12-15 23:33:35.774000

"""

# revision identifiers, used by Alembic.
revision = '33f4cda3c0bf'
down_revision = '216b3571df6c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=20), nullable=True))
    op.drop_index('nickname', table_name='user')
    op.create_unique_constraint(None, 'user', ['username'])
    op.drop_column('user', 'nickname')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('nickname', mysql.VARCHAR(length=20), nullable=True))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('nickname', 'user', ['nickname'], unique=True)
    op.drop_column('user', 'username')
    ### end Alembic commands ###