"""unique_column

Revision ID: 006feb00ef70
Revises: 22a5b35ab7f5
Create Date: 2023-02-14 16:48:50.321303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006feb00ef70'
down_revision = '22a5b35ab7f5'
branch_labels = None
depends_on = None

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('director', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
        batch_op.create_unique_constraint('fk_director_name', ['name'])

    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.create_unique_constraint('fk_film_name', ['name'])

    with op.batch_alter_table('genre', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
        batch_op.create_unique_constraint('fk_genre_name', ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('genre', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)

    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('director', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)

    # ### end Alembic commands ###
