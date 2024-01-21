"""empty message

Revision ID: 19f368a6e3b9
Revises: 
Create Date: 2024-01-21 10:26:57.348840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19f368a6e3b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    with op.batch_alter_table('loans', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'books_updated', ['bookID'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('loans', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'books', ['bookID'], ['id'])

    op.create_table('books',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=80), nullable=False),
    sa.Column('author', sa.VARCHAR(length=80), nullable=False),
    sa.Column('year', sa.INTEGER(), nullable=False),
    sa.Column('available', sa.BOOLEAN(), nullable=False),
    sa.Column('loan_type', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###