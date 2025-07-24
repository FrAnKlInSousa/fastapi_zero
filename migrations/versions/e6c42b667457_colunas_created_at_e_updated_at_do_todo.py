"""colunas created_at e updated_at do Todo

Revision ID: e6c42b667457
Revises: 3c7745fab18b
Create Date: 2025-07-24 12:34:06.227647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6c42b667457'
down_revision: Union[str, Sequence[str], None] = '3c7745fab18b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### comandos ajustados manualmente ###
    with op.batch_alter_table(
        'todos', schema=None
    ) as batch_op:

        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    # ### comandos ajustados manualmente ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
