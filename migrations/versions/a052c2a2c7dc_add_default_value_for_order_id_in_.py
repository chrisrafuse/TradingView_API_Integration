"""Add default value for order_id in webhooks

Revision ID: a052c2a2c7dc
Revises: afb946e2ad2e
Create Date: 2025-05-02 06:08:47.113336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a052c2a2c7dc'
down_revision: Union[str, None] = 'afb946e2ad2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create a new table with the updated schema
    op.create_table(
        'webhooks_new',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='polling'),
        sa.Column('limit_price', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('order_id', sa.String(), nullable=False, server_default='placeholder'),
    )

    # Copy data from the old table to the new table
    op.execute("""
        INSERT INTO webhooks_new (id, ticker, action, quantity, price, date, status, limit_price, order_id)
        SELECT id, ticker, action, quantity, price, date, status, limit_price, COALESCE(order_id, 'placeholder')
        FROM webhooks
    """)

    # Drop the old table
    op.drop_table('webhooks')

    # Rename the new table to the original table name
    op.rename_table('webhooks_new', 'webhooks')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate the old table
    op.create_table(
        'webhooks_old',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('limit_price', sa.Float(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=True),  # Allow NULL for downgrade
    )

    # Copy data back to the old table
    op.execute("""
        INSERT INTO webhooks_old (id, ticker, action, quantity, price, date, status, limit_price, order_id)
        SELECT id, ticker, action, quantity, price, date, status, limit_price, order_id
        FROM webhooks
    """)

    # Drop the current table
    op.drop_table('webhooks')

    # Rename the old table back to the original name
    op.rename_table('webhooks_old', 'webhooks')
