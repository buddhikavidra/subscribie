"""empty message

Revision ID: fa3e8029d9cb
Revises: 1928f415df34
Create Date: 2020-05-20 21:23:23.147552

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = 'fa3e8029d9cb'
down_revision = '1928f415df34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()                                                         
    inspector = Inspector.from_engine(conn)                                      
    tables = inspector.get_table_names() 

    if 'module_seo_page_title' in tables:
        op.drop_table('module_seo_page_title')

    if 'ding' in tables:
        op.drop_table('ding')

    if 'site' in tables:
        op.drop_table('site')

    if 'data' in tables:
        op.drop_table('data')

    if 'onboard_item' in tables:
        op.drop_table('onboard_item')

    if 'version' in tables:
        op.drop_table('version')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('version',
    sa.Column('pk', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('ding_id', sa.VARCHAR(), nullable=True),
    sa.Column('creator', sa.VARCHAR(), nullable=True),
    sa.Column('creation_date', sa.VARCHAR(), nullable=True),
    sa.Column('comment', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_table('onboard_item',
    sa.Column('name', sa.TEXT(), nullable=True),
    sa.Column('complete', sa.BOOLEAN(), server_default=sa.text('0'), nullable=True)
    )
    op.create_table('data',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ding_id', sa.VARCHAR(), nullable=True),
    sa.Column('version_id', sa.VARCHAR(), nullable=True),
    sa.Column('key', sa.VARCHAR(), nullable=True),
    sa.Column('value', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('site',
    sa.Column('site_id', sa.INTEGER(), nullable=False),
    sa.Column('site_path', sa.TEXT(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('active', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('site_id')
    )
    op.create_table('ding',
    sa.Column('pk', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('kind_id', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('pk')
    )
    op.create_table('module_seo_page_title',
    sa.Column('path', sa.TEXT(), nullable=False),
    sa.Column('title', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('path')
    )
    # ### end Alembic commands ###