import uuid
from datetime import datetime, timezone
from sqlmodel import Field, Column, SQLModel
from pydantic import computed_field
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy import ForeignKey, text
from backend.app.auth.schema import (
    BaseUserSchema,
    RoleChoicesSchema,
)  # ✅ fixed import name


class User(BaseUserSchema, table=True):
    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True),
        default_factory=uuid.uuid4,
    )
    hashed_password: str
    failed_login_attempts: int = Field(default=0, sa_type=pg.SMALLINT)
    last_failed_login: datetime | None = Field(
        default=None, sa_column=Column(pg.TIMESTAMP(timezone=True))
    )
    otp: str = Field(max_length=64, default="")
    otp_expiry_time: datetime | None = Field(
        default=None, sa_column=Column(pg.TIMESTAMP(timezone=True))
    )
    totp_secret: str | None = Field(default=None, max_length=255)
    is_totp_enabled: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP"),  # ✅ fixed
        ),
    )

    @computed_field
    @property
    def full_name(self) -> str:
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts).title()

    def has_role(self, role: RoleChoicesSchema) -> bool:  # ✅ renamed from role()
        return self.role.value == role.value
