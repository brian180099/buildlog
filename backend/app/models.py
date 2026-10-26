from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("length(nickname) BETWEEN 2 AND 20", name="ck_users_nickname_length"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)

    study_records: Mapped[list[StudyRecord]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    todo_items: Mapped[list[TodoItem]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    error_records: Mapped[list[ErrorRecord]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    comments: Mapped[list[Comment]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
    likes: Mapped[list[RecordLike]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    reports: Mapped[list[Report]] = relationship(
        back_populates="reporter", cascade="all, delete-orphan"
    )


class StudyRecord(TimestampMixin, Base):
    __tablename__ = "study_records"
    __table_args__ = (
        CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_study_title_length"),
        CheckConstraint("length(content) BETWEEN 1 AND 5000", name="ck_study_content_length"),
        Index("ix_study_author_created", "author_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    author: Mapped[User] = relationship(back_populates="study_records")
    comments: Mapped[list[Comment]] = relationship(
        back_populates="study_record", cascade="all, delete-orphan", passive_deletes=True
    )
    likes: Mapped[list[RecordLike]] = relationship(
        back_populates="study_record", cascade="all, delete-orphan", passive_deletes=True
    )


class TodoItem(TimestampMixin, Base):
    __tablename__ = "todo_items"
    __table_args__ = (
        CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_todo_title_length"),
        Index("ix_todo_author_status_created", "author_id", "is_completed", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    author: Mapped[User] = relationship(back_populates="todo_items")


class ErrorRecord(TimestampMixin, Base):
    __tablename__ = "error_records"
    __table_args__ = (
        CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_error_title_length"),
        CheckConstraint("length(content) BETWEEN 1 AND 5000", name="ck_error_content_length"),
        CheckConstraint(
            "resolution IS NULL OR length(resolution) BETWEEN 1 AND 5000",
            name="ck_error_resolution_length",
        ),
        CheckConstraint(
            "(is_resolved = false) OR (resolution IS NOT NULL AND length(resolution) > 0)",
            name="ck_error_resolution_required",
        ),
        Index("ix_error_author_status_created", "author_id", "is_resolved", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    author: Mapped[User] = relationship(back_populates="error_records")
    comments: Mapped[list[Comment]] = relationship(
        back_populates="error_record", cascade="all, delete-orphan", passive_deletes=True
    )
    likes: Mapped[list[RecordLike]] = relationship(
        back_populates="error_record", cascade="all, delete-orphan", passive_deletes=True
    )


class Comment(TimestampMixin, Base):
    __tablename__ = "comments"
    __table_args__ = (
        CheckConstraint("length(content) BETWEEN 1 AND 500", name="ck_comments_content_length"),
        CheckConstraint(
            "(study_record_id IS NOT NULL AND error_record_id IS NULL) OR "
            "(study_record_id IS NULL AND error_record_id IS NOT NULL)",
            name="ck_comments_exactly_one_target",
        ),
        Index("ix_comments_study_created", "study_record_id", "created_at"),
        Index("ix_comments_error_created", "error_record_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    study_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("study_records.id", ondelete="CASCADE"), nullable=True
    )
    error_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("error_records.id", ondelete="CASCADE"), nullable=True
    )
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    author: Mapped[User] = relationship(back_populates="comments")
    study_record: Mapped[StudyRecord | None] = relationship(back_populates="comments")
    error_record: Mapped[ErrorRecord | None] = relationship(back_populates="comments")


class RecordLike(Base):
    __tablename__ = "record_likes"
    __table_args__ = (
        CheckConstraint(
            "(study_record_id IS NOT NULL AND error_record_id IS NULL) OR "
            "(study_record_id IS NULL AND error_record_id IS NOT NULL)",
            name="ck_likes_exactly_one_target",
        ),
        UniqueConstraint(
            "user_id", "study_record_id", name="uq_likes_user_study_record"
        ),
        UniqueConstraint(
            "user_id", "error_record_id", name="uq_likes_user_error_record"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    study_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("study_records.id", ondelete="CASCADE"), nullable=True
    )
    error_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("error_records.id", ondelete="CASCADE"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    user: Mapped[User] = relationship(back_populates="likes")
    study_record: Mapped[StudyRecord | None] = relationship(back_populates="likes")
    error_record: Mapped[ErrorRecord | None] = relationship(back_populates="likes")


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        CheckConstraint(
            "target_type IN ('study_record', 'todo_item', 'error_record', 'comment')",
            name="ck_reports_target_type",
        ),
        CheckConstraint("length(reason) BETWEEN 1 AND 500", name="ck_reports_reason_length"),
        UniqueConstraint(
            "reporter_id", "target_type", "target_id", name="uq_reports_reporter_target"
        ),
        Index("ix_reports_created", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    reporter: Mapped[User] = relationship(back_populates="reports")

