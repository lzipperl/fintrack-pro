"""
FinTrack Pro - Subscription Module
Track recurring subscriptions (ORM-based)
"""

from datetime import date
from database import get_session
from models import Subscription


def add_subscription(name: str, amount: float, next_date: date) -> Subscription:
    """Add a new subscription."""
    session = get_session()
    try:
        sub = Subscription(name=name.strip(), amount=float(amount), next_date=next_date)
        session.add(sub)
        session.commit()
        session.refresh(sub)
        return sub
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def list_subscriptions():
    """List all subscriptions."""
    session = get_session()
    try:
        return session.query(Subscription).order_by(Subscription.next_date).all()
    finally:
        session.close()


def delete_subscription(sub_id: int) -> bool:
    """Delete a subscription by ID."""
    session = get_session()
    try:
        sub = session.query(Subscription).filter(Subscription.id == sub_id).first()
        if not sub:
            return False
        session.delete(sub)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
