from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    LargeBinary,
    String,
    Table,
    func,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship
from sqlalchemy import MetaData

from src.database import metadata

# metadata = MetaData()
mapper_registry = registry(metadata=metadata)
auth_user_t = Table(
    "auth_user",
    mapper_registry.metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

refresh_tokens_t = Table(
    "auth_refresh_token",
    mapper_registry.metadata,
    Column("uuid", UUID, primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

class AuthUserTable(object):
    pass

class RefreshTokensTable(object):
    pass


mapper_registry.map_imperatively(AuthUserTable, auth_user_t)
mapper_registry.map_imperatively(
    RefreshTokensTable, 
    refresh_tokens_t,     
    properties={
        "auth_users": relationship(AuthUserTable, backref="auth_user")
    },)
