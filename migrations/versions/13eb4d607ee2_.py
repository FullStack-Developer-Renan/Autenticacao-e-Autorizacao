"""empty message

Revision ID: 13eb4d607ee2
Revises: 
Create Date: 2021-07-12 09:55:35.494328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13eb4d607ee2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=127), nullable=False),
    sa.Column('last_name', sa.String(length=511), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=511), nullable=False),
    sa.Column('api_key', sa.VARCHAR(length=511), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Profiles')
    # ### end Alembic commands ###
