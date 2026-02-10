"""
FinTrack Pro - Report Module
Category-wise totals using raw SQL (GROUP BY, JOIN)
"""

from sqlalchemy import text
from database import get_session


def category_analytics():
    """
    Category-wise total spending using raw SQL:
    SELECT c.name, SUM(e.amount) FROM categories c
    JOIN expenses e ON c.id = e.category_id
    GROUP BY c.name;
    """
    session = get_session()
    try:
        sql = text("""
            SELECT c.name, SUM(e.amount) AS total
            FROM categories c
            JOIN expenses e ON c.id = e.category_id
            GROUP BY c.name
            ORDER BY total DESC
        """)
        result = session.execute(sql)
        rows = result.fetchall()
        return [(row[0], float(row[1])) for row in rows]
    finally:
        session.close()


def category_analytics_for_month(year_month: str):
    """Category-wise total for a specific month (YYYY-MM)."""
    session = get_session()
    try:
        sql = text("""
            SELECT c.name, SUM(e.amount) AS total
            FROM categories c
            JOIN expenses e ON c.id = e.category_id
            WHERE strftime('%Y-%m', e.date) = :ym
            GROUP BY c.name
            ORDER BY total DESC
        """)
        result = session.execute(sql, {"ym": year_month})
        rows = result.fetchall()
        return [(row[0], float(row[1])) for row in rows]
    finally:
        session.close()


def total_spending():
    """Total of all expenses (raw SQL)."""
    session = get_session()
    try:
        result = session.execute(text("SELECT COALESCE(SUM(amount), 0) FROM expenses"))
        return float(result.scalar())
    finally:
        session.close()


def total_spending_for_month(year_month: str) -> float:
    """Total spending for a given month (YYYY-MM)."""
    session = get_session()
    try:
        result = session.execute(
            text("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE strftime('%Y-%m', date) = :ym"),
            {"ym": year_month},
        )
        return float(result.scalar())
    finally:
        session.close()
