"""Initial revision

Revision ID: 87f91e966f79
Revises: 
Create Date: 2024-10-29 15:42:57.449094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87f91e966f79'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('chat_name', sa.String(), nullable=False),
    sa.Column('users_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('chat_id')
    )
    op.create_table('tg_users',
    sa.Column('tg_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('tg_id')
    )
    op.create_table('vk_users',
    sa.Column('vk_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('education', sa.String(), nullable=True),
    sa.Column('family_status', sa.String(), nullable=True),
    sa.Column('friends', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('groups', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('vk_id')
    )
    op.create_table('tg_interactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Enum('tag', 'react', 'message', 'add_user', name='tgactionenum', create_type=False), nullable=False),
    sa.Column('action_from', sa.Integer(), nullable=False),
    sa.Column('action_to', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['action_from'], ['tg_users.tg_id'], ),
    sa.ForeignKeyConstraint(['action_to'], ['tg_users.tg_id'], ),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.chat_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vk_id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['tg_id'], ['tg_users.tg_id'], ),
    sa.ForeignKeyConstraint(['vk_id'], ['vk_users.vk_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('music', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('posted_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['posted_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('vk_interactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Enum('like', 'comment', name='vkactionenum', create_type=False), nullable=False),
    sa.Column('action_from', sa.Integer(), nullable=False),
    sa.Column('action_to', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['action_from'], ['vk_users.vk_id'], ),
    sa.ForeignKeyConstraint(['action_to'], ['vk_users.vk_id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vk_interactions')
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('tg_interactions')
    op.drop_table('vk_users')
    op.drop_table('tg_users')
    op.drop_table('chats')
    # ### end Alembic commands ###
    op.execute('DROP TYPE IF EXISTS vkactionenum')
    op.execute('DROP TYPE IF EXISTS tgactionenum')