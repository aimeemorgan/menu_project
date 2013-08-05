"""adding tables to persist similarity relationships

Revision ID: 3897d5ead47a
Revises: 4ce1b92c6b43
Create Date: 2013-08-04 15:11:25.333521

"""

# revision identifiers, used by Alembic.
revision = '3897d5ead47a'
down_revision = '4ce1b92c6b43'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurantsimilarities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id_1', sa.Integer(), nullable=False),
    sa.Column('restaurant_id_2', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id_1'], ['restaurants.id'], ),
    sa.ForeignKeyConstraint(['restaurant_id_2'], ['restaurants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('menusimilarities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('menu_id_1', sa.Integer(), nullable=False),
    sa.Column('menu_id_2', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id_1'], ['menus.id'], ),
    sa.ForeignKeyConstraint(['menu_id_2'], ['menus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('itemsimilarities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id_1', sa.Integer(), nullable=False),
    sa.Column('item_id_2', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id_1'], ['items.id'], ),
    sa.ForeignKeyConstraint(['item_id_2'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('itemsimilarities')
    op.drop_table('menusimilarities')
    op.drop_table('restaurantsimilarities')
    ### end Alembic commands ###
