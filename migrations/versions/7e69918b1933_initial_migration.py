"""initial migration

Revision ID: 7e69918b1933
Revises: None
Create Date: 2016-03-27 23:49:10.651000

"""

# revision identifiers, used by Alembic.
revision = '7e69918b1933'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('college_course', sa.Column('lecturer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'college_course', 'lecturer', ['lecturer_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'college_course', type_='foreignkey')
    op.drop_column('college_course', 'lecturer_id')
    ### end Alembic commands ###
