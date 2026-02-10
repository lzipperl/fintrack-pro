"""
FinTrack Pro – CLI Finance Manager
Personal finance management: expenses, subscriptions, budgets, analytics
"""

from datetime import date, datetime
import sys
import os

# Ensure src is on path when run from project root or from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_session
from expense_module import (
    list_categories,
    add_expense,
    update_expense,
    delete_expense,
    get_expense_by_id,
    list_recent_expenses,
)
from report_module import category_analytics, category_analytics_for_month, total_spending, total_spending_for_month
from budget_module import set_budget, get_budget, check_budget_alert
from search_module import search_by_date, search_by_date_range
from subscription_module import add_subscription, list_subscriptions, delete_subscription


def parse_date(s: str) -> date | None:
    """Parse YYYY-MM-DD or DD/MM/YYYY to date."""
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_month(s: str) -> str | None:
    """Parse to YYYY-MM."""
    s = s.strip()
    if len(s) == 7 and s[4] == "-":
        try:
            datetime.strptime(s + "-01", "%Y-%m-%d")
            return s
        except ValueError:
            pass
    try:
        d = datetime.strptime(s, "%Y-%m")
        return d.strftime("%Y-%m")
    except ValueError:
        return None


def print_header(title: str):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def run_add_expense():
    print_header("Add Expense")
    session = get_session()
    try:
        categories = list_categories(session)
        if not categories:
            print("No categories found. Run the app once to seed defaults.")
            return
        for i, c in enumerate(categories, 1):
            print(f"  {i}. {c.name}")
        cat_choice = input("Category number: ").strip()
        try:
            idx = int(cat_choice)
            if 1 <= idx <= len(categories):
                category_id = categories[idx - 1].id
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Enter a number.")
            return

        title = input("Title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
        amount_str = input("Amount: ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            print(f"Invalid amount: {e}")
            return
        date_str = input("Date (YYYY-MM-DD or DD/MM/YYYY) [today]: ").strip()
        expense_date = date.today()
        if date_str:
            expense_date = parse_date(date_str)
            if not expense_date:
                print("Invalid date.")
                return
        exp = add_expense(title, amount, expense_date, category_id)
        print(f"Added expense: {exp.title} - {exp.amount:.2f} on {exp.date}")
    finally:
        session.close()


def run_update_expense():
    print_header("Update Expense")
    recent = list_recent_expenses(10)
    if not recent:
        print("No expenses to update.")
        return
    for e in recent:
        cat_name = e.category.name if e.category else "?"
        print(f"  {e.id}. {e.title} | {e.amount:.2f} | {e.date} | {cat_name}")
    eid_str = input("Expense ID to update: ").strip()
    try:
        eid = int(eid_str)
    except ValueError:
        print("Invalid ID.")
        return
    exp = get_expense_by_id(eid)
    if not exp:
        print("Expense not found.")
        return
    print(f"Current: {exp.title}, {exp.amount}, {exp.date}")
    title = input("New title (Enter to keep): ").strip()
    amount_str = input("New amount (Enter to keep): ").strip()
    date_str = input("New date YYYY-MM-DD (Enter to keep): ").strip()
    session = get_session()
    try:
        categories = list_categories(session)
        print("Categories:", [f"{c.id}:{c.name}" for c in categories])
        cat_str = input("New category_id (Enter to keep): ").strip()
    finally:
        session.close()
    category_id = int(cat_str) if cat_str.isdigit() else None
    expense_date = parse_date(date_str) if date_str else None
    amount = float(amount_str) if amount_str else None
    updated = update_expense(eid, title or None, amount, expense_date, category_id)
    if updated:
        print(f"Updated: {updated.title} - {updated.amount:.2f} on {updated.date}")


def run_delete_expense():
    print_header("Delete Expense")
    recent = list_recent_expenses(15)
    if not recent:
        print("No expenses.")
        return
    for e in recent:
        print(f"  {e.id}. {e.title} | {e.amount:.2f} | {e.date}")
    eid_str = input("Expense ID to delete: ").strip()
    try:
        eid = int(eid_str)
    except ValueError:
        print("Invalid ID.")
        return
    if delete_expense(eid):
        print("Expense deleted.")
    else:
        print("Expense not found.")


def run_search_by_date():
    print_header("Search by Date")
    date_str = input("Date (YYYY-MM-DD or DD/MM/YYYY): ").strip()
    if not date_str:
        print("Date required.")
        return
    d = parse_date(date_str)
    if not d:
        print("Invalid date.")
        return
    rows = search_by_date(d)
    if not rows:
        print(f"No expenses on {d}")
        return
    print(f"Expenses on {d}:")
    total = 0
    for r in rows:
        print(f"  ID {r[0]}: {r[1]} - {r[2]:.2f} ({r[4]})")
        total += r[2]
    print(f"  Total: {total:.2f}")


def run_category_analytics():
    print_header("Category Analytics")
    month_str = input("Month YYYY-MM (Enter for all time): ").strip()
    if month_str:
        ym = parse_month(month_str)
        if not ym:
            print("Invalid month. Use YYYY-MM.")
            return
        rows = category_analytics_for_month(ym)
        total = total_spending_for_month(ym)
    else:
        rows = category_analytics()
        total = total_spending()
    if not rows:
        print("No expenses in this period.")
        return
    for name, tot in rows:
        print(f"  {name}: {tot:.2f}")
    print(f"  TOTAL: {total:.2f}")


def run_monthly_budget_alert():
    print_header("Monthly Budget Alert")
    month_str = input("Month (YYYY-MM) [current]: ").strip()
    ym = datetime.now().strftime("%Y-%m") if not month_str else parse_month(month_str or datetime.now().strftime("%Y-%m"))
    if not ym:
        ym = datetime.now().strftime("%Y-%m")
    result = check_budget_alert(ym)
    print(result["message"])
    if result["exceeded"]:
        print("  >>> Budget exceeded! <<<")


def run_set_budget():
    print_header("Set Monthly Budget")
    month_str = input("Month (YYYY-MM): ").strip() or datetime.now().strftime("%Y-%m")
    ym = parse_month(month_str)
    if not ym:
        print("Invalid month. Use YYYY-MM.")
        return
    limit_str = input("Budget limit: ").strip()
    try:
        limit = float(limit_str)
        if limit <= 0:
            raise ValueError("Limit must be positive")
    except ValueError as e:
        print(f"Invalid limit: {e}")
        return
    set_budget(ym, limit)
    print(f"Budget for {ym} set to {limit:.2f}")


def run_list_recent():
    print_header("Recent Expenses")
    expenses = list_recent_expenses(20)
    if not expenses:
        print("No expenses yet.")
        return
    for e in expenses:
        cat = e.category.name if e.category else "?"
        print(f"  {e.id}. {e.date} | {e.title} | {e.amount:.2f} | {cat}")


def run_subscriptions():
    print_header("Subscriptions")
    print("1. List  2. Add  3. Delete")
    choice = input("Choice: ").strip()
    if choice == "1":
        subs = list_subscriptions()
        if not subs:
            print("No subscriptions.")
            return
        for s in subs:
            print(f"  {s.id}. {s.name} - {s.amount:.2f} (next: {s.next_date})")
    elif choice == "2":
        name = input("Name: ").strip()
        amount_str = input("Amount: ").strip()
        date_str = input("Next date (YYYY-MM-DD): ").strip()
        if not name or not amount_str or not date_str:
            print("All fields required.")
            return
        d = parse_date(date_str)
        if not d:
            print("Invalid date.")
            return
        try:
            add_subscription(name, float(amount_str), d)
            print("Subscription added.")
        except Exception as e:
            print(f"Error: {e}")
    elif choice == "3":
        subs = list_subscriptions()
        for s in subs:
            print(f"  {s.id}. {s.name}")
        sid = input("Subscription ID to delete: ").strip()
        if sid.isdigit() and delete_subscription(int(sid)):
            print("Deleted.")
        else:
            print("Not found or invalid ID.")


def main():
    init_db()
    print("\n  FinTrack Pro – CLI Finance Manager")
    print("  --------------------------------")
    while True:
        print("\n  1. Add Expense")
        print("  2. Update Expense")
        print("  3. Delete Expense")
        print("  4. Search by Date")
        print("  5. Category Analytics")
        print("  6. Monthly Budget Alert")
        print("  7. Set Monthly Budget")
        print("  8. Recent Expenses")
        print("  9. Subscriptions")
        print("  0. Exit")
        choice = input("\nChoice: ").strip()
        if choice == "1":
            run_add_expense()
        elif choice == "2":
            run_update_expense()
        elif choice == "3":
            run_delete_expense()
        elif choice == "4":
            run_search_by_date()
        elif choice == "5":
            run_category_analytics()
        elif choice == "6":
            run_monthly_budget_alert()
        elif choice == "7":
            run_set_budget()
        elif choice == "8":
            run_list_recent()
        elif choice == "9":
            run_subscriptions()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
