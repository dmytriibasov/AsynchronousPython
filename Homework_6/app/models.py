import uuid
from datetime import datetime

from sqlalchemy import String, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    def __iter__(self):
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("_sa_")}
        yield from data.items()


class CVERecord(Base):
    __tablename__ = "cve_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    cve_id: Mapped[str] = mapped_column(String(length=255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(length=255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    published_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self) -> str:
        return f"<{self.cve_id}, internal_id={self.id})>"
