from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.models.base import Base

# ---------------------------------------------------------------------
# Import all models so SQLAlchemy registers them
# ---------------------------------------------------------------------

# Catalog
import app.models.catalog.product
import app.models.catalog.product_variant
import app.models.catalog.brand
import app.models.catalog.category
import app.models.catalog.inventory

# Customer
import app.models.customer.customer
import app.models.customer.address

# Conversation
import app.models.conversation.session
import app.models.conversation.message

# Draft
import app.models.draft.draft
import app.models.draft.draft_item

# Order
import app.models.order.order
import app.models.order.order_item
import app.models.order.payment
import app.models.order.shipment
import app.models.order.order_status_history

# ---------------------------------------------------------------------
# Alembic Config
# ---------------------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# ---------------------------------------------------------------------
# Offline Migrations
# ---------------------------------------------------------------------


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------
# Online Migrations
# ---------------------------------------------------------------------


def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()