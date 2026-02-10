"""
FinTrack Pro - Budget Module
Set monthly limit, compare with spending, alert when exceeded
"""

from sqlalchemy.orm import Session
from database import get_session
from models import Budget
from report_module import total_spending_for_month


def set_budget(month: str, limit: float) -> Budget:
    """Set or update monthly budget (month format: YYYY-MM)."""
    session = get_session()
    try:
        budget = session.query(Budget).filter(Budget.month == month).first()
        if budget:
            budget.limit = float(limit)
        else:
            budget = Budget(month=month, limit=float(limit))
            session.add(budget)
        session.commit()
        session.refresh(budget)
        return budget
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_budget(month: str) -> Budget | None:
    """Get budget for a month (YYYY-MM)."""
    session = get_session()
    try:
        return session.query(Budget).filter(Budget.month == month).first()
    finally:
        session.close()


def check_budget_alert(month: str) -> dict:
    """
    Compare spending with budget for the month.
    Returns: { "month", "limit", "spent", "remaining", "exceeded", "message" }
    """
    budget = get_budget(month)
    spent = total_spending_for_month(month)

    if not budget:
        return {
            "month": month,
            "limit": None,
            "spent": spent,
            "remaining": None,
            "exceeded": False,
            "message": f"No budget set for {month}. Total spent: {spent:.2f}",
        }

    limit = budget.limit
    remaining = limit - spent
    exceeded = spent > limit

    if exceeded:
        message = f"ALERT: Budget exceeded for {month}! Limit: {limit:.2f}, Spent: {spent:.2f} (Over by {remaining:.2f})"
    else:
        message = f"Within budget for {month}. Spent: {spent:.2f} / {limit:.2f}, Remaining: {remaining:.2f}"

    return {
        "month": month,
        "limit": limit,
        "spent": spent,
        "remaining": remaining,
        "exceeded": exceeded,
        "message": message,
    }


def list_all_budgets():
    """List all budget records."""
    session = get_session()
    try:
        return session.query(Budget).order_by(Budget.month.desc()).all()
    finally:
        session.close()
