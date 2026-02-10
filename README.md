# FinTrack Pro – CLI Finance Manager

A command-line personal finance management system built with **Python**, **SQLite**, and **SQLAlchemy ORM**. Manage expenses, track subscriptions, set budgets, and view category analytics using both ORM and raw SQL.

## Features

- **Add / Update / Delete Expense** – ORM-based CRUD
- **Search by Date** – Find expenses by date (SQL query)
- **Category Analytics** – Totals by category (raw SQL with `GROUP BY` and `JOIN`)
- **Monthly Budget** – Set a limit and get an alert when exceeded
- **Subscriptions** – Track recurring subscriptions
- **Persistent Storage** – SQLite database (`fintrack.db`)

## Technologies

- Python 3
- SQLite
- SQLAlchemy ORM
- Raw SQL for reports and search

## Setup

```bash
cd fintrack-pro
pip install -r requirements.txt
```

## Run

From project root:

```bash
python src/main.py
```

Or from inside `src`:

```bash
cd src
python main.py
```

## Database

- **Location:** `fintrack.db` in the project root (created on first run).
- **Tables:** `categories`, `expenses`, `subscriptions`, `budgets`
- Default categories are seeded on first run: Food, Transport, Utilities, Entertainment, Shopping, Health, Other.

## Menu Options

1. Add Expense  
2. Update Expense  
3. Delete Expense  
4. Search by Date  
5. Category Analytics  
6. Monthly Budget Alert  
7. Set Monthly Budget  
8. Recent Expenses  
9. Subscriptions  
0. Exit  

## Sample SQL (Category Analytics)

```sql
SELECT c.name, SUM(e.amount)
FROM categories c
JOIN expenses e ON c.id = e.category_id
GROUP BY c.name;
```

## Learning Outcomes

- ORM usage with SQLAlchemy  
- SQL joins and aggregation  
- Modular structure and exception handling  
- CLI application design  

## Future Enhancements

- CSV export  
- Flask web UI  
- Authentication  
- Charts  

---

*FinTrack Pro – suitable for portfolio and interview discussion.*
