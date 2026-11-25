"""Replace the cash ledger with instrument positions.

Revision ID: c4a1b2d3e5f6
Revises: f6f99966b836
Create Date: 2026-11-25 11:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "c4a1b2d3e5f6"
down_revision = "f6f99966b836"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("transactions")
    op.drop_table("portfolios")
    op.drop_table("users")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "portfolios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("client_name", sa.String(length=100), nullable=False),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_portfolios_owner_id", "portfolios", ["owner_id"], unique=False)

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("portfolio_id", sa.Integer(), nullable=False),
        sa.Column("instrument", sa.String(length=20), nullable=False),
        sa.Column("type", sa.String(length=4), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column("unit_price", sa.Numeric(precision=18, scale=4), nullable=False),
        sa.Column("trade_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("quantity > 0", name="ck_transactions_quantity_positive"),
        sa.CheckConstraint("unit_price > 0", name="ck_transactions_price_positive"),
        sa.CheckConstraint("type IN ('BUY','SELL')", name="ck_transactions_type"),
        sa.ForeignKeyConstraint(["portfolio_id"], ["portfolios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_transactions_portfolio_id", "transactions", ["portfolio_id"], unique=False)
    op.create_index("ix_transactions_instrument", "transactions", ["instrument"], unique=False)
    op.create_index("ix_transactions_trade_date", "transactions", ["trade_date"], unique=False)


def downgrade():
    op.drop_index("ix_transactions_trade_date", table_name="transactions")
    op.drop_index("ix_transactions_instrument", table_name="transactions")
    op.drop_index("ix_transactions_portfolio_id", table_name="transactions")
    op.drop_table("transactions")
    op.drop_index("ix_portfolios_owner_id", table_name="portfolios")
    op.drop_table("portfolios")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
