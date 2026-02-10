"""
FinTrack Pro - Search Module
Find expenses by date using SQL
"""

from datetime import date
from sqlalchemy import text
from database import get_session


def search_by_date(expense_date: date) -> list[tuple]:
    """
    Search expenses by exact date using raw SQL.
    Returns list of (id, title, amount, date, category_name).
    """
    session = get_session()
    try:
        sql = text("""
            SELECT e.id, e.title, e.amount, e.date, c.name AS category_name
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.date = :d
            ORDER BY e.id
        """)
        result = session.execute(sql, {"d": expense_date.isoformat()})
        return result.fetchall()
    finally:
        session.close()


def search_by_date_range(start_date: date, end_date: date) -> list[tuple]:
    """Search expenses within a date range. Same column format as search_by_date."""
    session = get_session()
    try:
        sql = text("""
            SELECT e.id, e.title, e.amount, e.date, c.name AS category_name
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.date BETWEEN :start AND :end
            ORDER BY e.date, e.id
        """)
        result = session.execute(
            sql,
            {"start": start_date.isoformat(), "end": end_date.isoformat()},
        )
        return result.fetchall()
    finally:
        session.close()
