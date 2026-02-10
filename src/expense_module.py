"""
FinTrack Pro - Expense Module
ORM-based CRUD: Add, Update, Delete expenses
"""

from datetime import date
from sqlalchemy.orm import Session
from models import Expense, Category
from database import get_session


def list_categories(session: Session) -> list[Category]:
    """Return all categories for selection."""
    return session.query(Category).order_by(Category.name).all()


def add_expense(title: str, amount: float, expense_date: date, category_id: int) -> Expense | None:
    """Add a new expense. Returns the created expense or None on error."""
    session = get_session()
    try:
        expense = Expense(
            title=title.strip(),
            amount=float(amount),
            date=expense_date,
            category_id=int(category_id),
        )
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_expense(expense_id: int, title: str = None, amount: float = None,
                   expense_date: date = None, category_id: int = None) -> Expense | None:
    """Update an existing expense. Only provided fields are updated."""
    session = get_session()
    try:
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            return None
        if title is not None:
            expense.title = title.strip()
        if amount is not None:
            expense.amount = float(amount)
        if expense_date is not None:
            expense.date = expense_date
        if category_id is not None:
            expense.category_id = int(category_id)
        session.commit()
        session.refresh(expense)
        return expense
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_expense(expense_id: int) -> bool:
    """Delete an expense by ID. Returns True if deleted, False if not found."""
    session = get_session()
    try:
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            return False
        session.delete(expense)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_expense_by_id(expense_id: int) -> Expense | None:
    """Fetch a single expense by ID."""
    session = get_session()
    try:
        return session.query(Expense).filter(Expense.id == expense_id).first()
    finally:
        session.close()


def list_recent_expenses(limit: int = 20) -> list[Expense]:
    """List recent expenses with category name (for CLI display)."""
    session = get_session()
    try:
        return (
            session.query(Expense)
            .order_by(Expense.date.desc(), Expense.id.desc())
            .limit(limit)
            .all()
        )
    finally:
        session.close()
