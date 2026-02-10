"""
FinTrack Pro - SQLAlchemy ORM Models
Database: SQLite
Tables: categories, expenses, subscriptions, budgets
"""

from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Category(Base):
    """Category table: id, name"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationship: Category 1 ---- N Expenses
    expenses = relationship("Expense", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Expense(Base):
    """Expense table: id, title, amount, date, category_id"""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(id={self.id}, title='{self.title}', amount={self.amount})>"


class Subscription(Base):
    """Subscription table: id, name, amount, next_date"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    next_date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Subscription(id={self.id}, name='{self.name}', amount={self.amount})>"


class Budget(Base):
    """Budget table: id, month, limit"""
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String(7), nullable=False, unique=True)  # Format: YYYY-MM
    limit = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Budget(month='{self.month}', limit={self.limit})>"
