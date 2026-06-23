from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    applications: Mapped[list["Application"]] = relationship(back_populates="user")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    project_type: Mapped[str] = mapped_column(String(120))
    has_spec: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    budget: Mapped[str] = mapped_column(String(120))
    deadline: Mapped[str] = mapped_column(String(120))
    contact: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(60), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="applications")


class PortfolioCategory(Base):
    __tablename__ = "portfolio_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cases: Mapped[list["PortfolioCase"]] = relationship(back_populates="category")


class PortfolioCase(Base):
    __tablename__ = "portfolio_cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("portfolio_categories.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category: Mapped[PortfolioCategory] = relationship(back_populates="cases")

