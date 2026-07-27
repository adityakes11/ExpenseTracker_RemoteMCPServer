from fastmcp import FastMCP
import sqlite3
import json
import csv
import shutil
import os

from database import init_db, get_connection
from utils import validate_amount, validate_date

BASE_DIR = os.path.dirname(__file__)

CATEGORY_PATH = os.path.join(BASE_DIR, "categories.json")

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

    validate_date(date)
    amount = validate_amount(amount)

    conn = get_connection()

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

    expense_id = cur.lastrowid

    conn.close()

    return {
        "status": "success",
        "expense_id": expense_id
    }

@mcp.tool()
def list_expenses(start_date: str, end_date: str):
    """
    List all expenses within a date range.
    """

    validate_date(start_date)
    validate_date(end_date)

    conn = get_connection()

    cur = conn.execute("""
        SELECT *
        FROM expenses
        WHERE date BETWEEN ? AND ?
        ORDER BY date
    """, (start_date, end_date))

    rows = [dict(r) for r in cur.fetchall()]

    conn.close()

    return rows

@mcp.tool()
def get_expense(expense_id: int):
    """
    Retrieve one expense.
    """

    conn = get_connection()

    cur = conn.execute("""
        SELECT *
        FROM expenses
        WHERE id=?
    """, (expense_id,))

    row = cur.fetchone()

    conn.close()

    if row is None:
        return {"error": "Expense not found"}

    return dict(row)

@mcp.tool()
def delete_expense(expense_id: int):
    """
    Delete an expense.
    """

    conn = get_connection()

    conn.execute("""
        DELETE FROM expenses
        WHERE id=?
    """, (expense_id,))

    conn.commit()

    conn.close()

    return {"status": "deleted"}

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

    validate_date(date)
    amount = validate_amount(amount)

    conn = get_connection()

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

    conn.close()

    return {"status": "updated"}

@mcp.tool()
def search_expenses(keyword: str):
    """
    Search expenses by category, subcategory, merchant, or note.
    """

    conn = get_connection()

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

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows

@mcp.tool()
def summarize(start_date: str, end_date: str):
    """
    Summarize expenses by category.
    """

    validate_date(start_date)
    validate_date(end_date)

    conn = get_connection()

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

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows

@mcp.tool()
def total_spending(start_date: str, end_date: str):
    """
    Calculate total spending in a date range.
    """

    validate_date(start_date)
    validate_date(end_date)

    conn = get_connection()

    cur = conn.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        WHERE date BETWEEN ? AND ?
        """,
        (start_date, end_date),
    )

    total = cur.fetchone()[0] or 0

    conn.close()

    return {"total": total}

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open(CATEGORY_PATH, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()    