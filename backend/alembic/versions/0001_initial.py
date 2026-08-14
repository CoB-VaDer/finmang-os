"""initial FinMang OS schema"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    account_type = sa.Enum("CHECKING", "SAVINGS", "CREDIT", "CASH", "E_WALLET", name="account_type")
    category_type = sa.Enum("INCOME", "EXPENSE", name="category_type")
    transaction_type = sa.Enum("INCOME", "EXPENSE", "TRANSFER", name="transaction_type")
    account_type.create(op.get_bind(), checkfirst=True); category_type.create(op.get_bind(), checkfirst=True); transaction_type.create(op.get_bind(), checkfirst=True)
    op.create_table("accounts", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("name", sa.String(100), nullable=False), sa.Column("type", account_type, nullable=False), sa.Column("balance", sa.Numeric(15,2), nullable=False, server_default="0.00"), sa.Column("currency", sa.String(3), nullable=False), sa.Column("institution", sa.String(100)), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("categories", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("name", sa.String(50), nullable=False), sa.Column("type", category_type, nullable=False), sa.Column("parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("categories.id", ondelete="SET NULL")), sa.Column("color", sa.String(7)), sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.false()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("transactions", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False), sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False), sa.Column("amount", sa.Numeric(15,2), nullable=False), sa.Column("type", transaction_type, nullable=False), sa.Column("description", sa.String(255)), sa.Column("transaction_date", sa.Date(), nullable=False), sa.Column("is_reconciled", sa.Boolean(), nullable=False, server_default=sa.false()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.CheckConstraint("amount > 0", name="ck_transactions_amount_positive"))
    op.create_index("ix_transactions_date", "transactions", ["transaction_date"])
    op.create_table("audit_logs", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("action", sa.String(50), nullable=False), sa.Column("entity_type", sa.String(50), nullable=False), sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("details", postgresql.JSONB()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))

def downgrade():
    op.drop_table("audit_logs"); op.drop_index("ix_transactions_date", table_name="transactions"); op.drop_table("transactions"); op.drop_table("categories"); op.drop_table("accounts")
    for name in ("transaction_type", "category_type", "account_type"): sa.Enum(name=name).drop(op.get_bind(), checkfirst=True)
