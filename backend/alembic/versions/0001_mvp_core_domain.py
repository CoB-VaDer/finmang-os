from alembic import op
import sqlalchemy as sa

revision = "0001_mvp_core_domain"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    account_type = sa.Enum("asset", "liability", "cash", "bank", name="account_type")
    category_type = sa.Enum("income", "expense", name="category_type")
    transaction_type = sa.Enum("income", "expense", "transfer", name="transaction_type")
    bind = op.get_bind()
    account_type.create(bind, checkfirst=True)
    category_type.create(bind, checkfirst=True)
    transaction_type.create(bind, checkfirst=True)
    op.create_table("accounts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("account_type", sa.String(30), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.UniqueConstraint("name"))
    op.create_table("categories", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("category_type", sa.String(20), nullable=False), sa.Column("parent_id", sa.Integer(), sa.ForeignKey("categories.id")), sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.create_table("transactions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("account_id", sa.Integer(), sa.ForeignKey("accounts.id"), nullable=False), sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id"), nullable=False), sa.Column("transaction_type", sa.String(20), nullable=False), sa.Column("amount", sa.Numeric(14, 2), nullable=False), sa.Column("transaction_date", sa.Date(), nullable=False), sa.Column("note", sa.Text()))
    op.create_index("ix_transactions_account_date", "transactions", ["account_id", "transaction_date"])
    op.create_index("ix_transactions_category", "transactions", ["category_id"])
    op.create_index("ix_transactions_type_date", "transactions", ["transaction_type", "transaction_date"])


def downgrade():
    op.drop_index("ix_transactions_type_date", table_name="transactions")
    op.drop_index("ix_transactions_category", table_name="transactions")
    op.drop_index("ix_transactions_account_date", table_name="transactions")
    op.drop_table("transactions")
    op.drop_table("categories")
    op.drop_table("accounts")
    bind = op.get_bind()
    for name in ("transaction_type", "category_type", "account_type"):
        sa.Enum(name=name).drop(bind, checkfirst=True)
