"""empty message

Revision ID: aabeca5612c1
Revises: 9ffb76723b1c
Create Date: 2022-07-13 20:38:34.560282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aabeca5612c1'
down_revision = '9ffb76723b1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('poster_url', sa.String(length=500), nullable=True))
    op.add_column('streamingplatforms', sa.Column('logo_url', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('streamingplatforms', 'logo_url')
    op.drop_column('movies', 'poster_url')
    # ### end Alembic commands ###