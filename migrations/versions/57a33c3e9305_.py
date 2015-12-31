"""empty message

Revision ID: 57a33c3e9305
Revises: None
Create Date: 2015-12-31 20:45:30.034000

"""

# revision identifiers, used by Alembic.
revision = '57a33c3e9305'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'product', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'], ondelete=u'SET NULL')
    op.create_unique_constraint(None, 'user', ['cellphone'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column(u'product', 'category_id')
    op.drop_table('category')
    ### end Alembic commands ###