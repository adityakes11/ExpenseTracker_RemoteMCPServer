from fastmcp import FastMCP
import sqlite3
import json
import csv
import shutil
import os

from database import init_db, get_connection
from utils import validate_amount, validate_date, validate_category, CATEGORY_PATH

mcp = FastMCP("Expense Tracker")

init_db()

@mcp.tool()
def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    payment_method: str = "",
    merchant: str = "",
    note: str = ""
):
    """
    Add a new expense.
    """
    try:
        validate_date(date)
        amount = validate_amount(amount)
        validate_category(category, subcategory)

        with get_connection() as conn:
            cur = conn.execute("""
                INSERT INTO expenses(
                date,
                amount,
                category,
                subcategory,
                payment_method,
                merchant,
                note
                )
                VALUES(?,?,?,?,?,?,?)
            """, (
                date,
                amount,
                category,
                subcategory,
                payment_method,
                merchant,
                note
            ))
            conn.commit()
            return {"status": "success", "expense_id": cur.lastrowid}

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def list_expenses(start_date: str, end_date: str):
    """
    List all expenses within a date range.
    """
    try:
        validate_date(start_date)
        validate_date(end_date)

        with get_connection() as conn:
            cur = conn.execute("""
                SELECT *
                FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY date
            """, (start_date, end_date))
            return [dict(r) for r in cur.fetchall()]

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def get_expense(expense_id: int):
    """
    Retrieve one expense.
    """
    try:
        with get_connection() as conn:
            cur = conn.execute("""
                SELECT *
                FROM expenses
                WHERE id=?
            """, (expense_id,))
            row = cur.fetchone()

            if row is None:
                return {"error": "Expense not found"}
            return dict(row)

    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def delete_expense(expense_id: int):
    """
    Delete an expense.
    """
    try:
        with get_connection() as conn:
            conn.execute("""
                DELETE FROM expenses
                WHERE id=?
            """, (expense_id,))
            conn.commit()
            return {"status": "deleted"}

    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def update_expense(
    expense_id: int,
    date: str,
    amount: float,
    category: str,
    subcategory: str = "",
    payment_method: str = "",
    merchant: str = "",
    note: str = ""
):
    """
    Update an existing expense.
    """
    try:
        validate_date(date)
        amount = validate_amount(amount)
        validate_category(category, subcategory)

        with get_connection() as conn:
            conn.execute("""
                UPDATE expenses
                SET
                    date=?,
                    amount=?,
                    category=?,
                    subcategory=?,
                    payment_method=?,
                    merchant=?,
                    note=?
                WHERE id=?
            """, (
                date,
                amount,
                category,
                subcategory,
                payment_method,
                merchant,
                note,
                expense_id
            ))
            conn.commit()
            return {"status": "updated"}

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def search_expenses(keyword: str):
    """
    Search expenses by category, subcategory, merchant, or note.
    """
    try:
        with get_connection() as conn:
            cur = conn.execute(
                """
                SELECT *
                FROM expenses
                WHERE
                    category LIKE ?
                    OR subcategory LIKE ?
                    OR merchant LIKE ?
                    OR note LIKE ?
                ORDER BY date DESC
                """,
                (
                    f"%{keyword}%",
                    f"%{keyword}%",
                    f"%{keyword}%",
                    f"%{keyword}%"
                ),
            )
            return [dict(r) for r in cur.fetchall()]

    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def summarize(start_date: str, end_date: str):
    """
    Summarize expenses by category.
    """
    try:
        validate_date(start_date)
        validate_date(end_date)

        with get_connection() as conn:
            cur = conn.execute(
                """
                SELECT
                    category,
                    SUM(amount) AS total
                FROM expenses
                WHERE date BETWEEN ? AND ?
                GROUP BY category
                ORDER BY total DESC
                """,
                (start_date, end_date),
            )
            return [dict(r) for r in cur.fetchall()]

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def total_spending(start_date: str, end_date: str):
    """
    Calculate total spending in a date range.
    """
    try:
        validate_date(start_date)
        validate_date(end_date)

        with get_connection() as conn:
            cur = conn.execute(
                """
                SELECT SUM(amount)
                FROM expenses
                WHERE date BETWEEN ? AND ?
                """,
                (start_date, end_date),
            )
            total = cur.fetchone()[0] or 0
            return {"total": total}

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def set_budget(month: str, category: str, budget: float):
    """
    Set or update a budget for a specific month and category.
    Format for month: 'YYYY-MM'
    """
    try:
        budget = validate_amount(budget)
        validate_category(category)

        with get_connection() as conn:
            cur = conn.execute("SELECT id FROM budgets WHERE month=? AND category=?", (month, category))
            row = cur.fetchone()

            if row:
                conn.execute("UPDATE budgets SET budget=? WHERE id=?", (budget, row['id']))
            else:
                conn.execute("INSERT INTO budgets (month, category, budget) VALUES (?,?,?)", (month, category, budget))
            
            conn.commit()
            return {"status": "success", "message": f"Budget set for {category} in {month}"}

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def get_budgets(month: str):
    """
    List all budgets for a given month (format: 'YYYY-MM').
    """
    try:
        with get_connection() as conn:
            cur = conn.execute("SELECT category, budget FROM budgets WHERE month=?", (month,))
            return [dict(r) for r in cur.fetchall()]
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.tool()
def check_budget(month: str, category: str):
    """
    Check actual spending vs budget for a given month and category.
    Format for month: 'YYYY-MM'
    """
    try:
        validate_category(category)
        with get_connection() as conn:
            cur = conn.execute("SELECT budget FROM budgets WHERE month=? AND category=?", (month, category))
            b_row = cur.fetchone()
            budget_amt = b_row['budget'] if b_row else 0.0

            cur = conn.execute("""
                SELECT SUM(amount) FROM expenses 
                WHERE category=? AND date LIKE ?
            """, (category, f"{month}-%"))
            s_row = cur.fetchone()
            spent_amt = s_row[0] or 0.0

            return {
                "month": month,
                "category": category,
                "budget": budget_amt,
                "spent": spent_amt,
                "remaining": budget_amt - spent_amt
            }

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open(CATEGORY_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()