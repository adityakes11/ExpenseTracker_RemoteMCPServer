# Expense Tracker MCP Server

A lightweight **FastMCP** based server that provides a CRUD API for personal expense tracking. The server stores expenses in a local SQLite database and exposes a set of tools (MCP‑compatible functions) that can be called remotely – e.g., from a chatbot, automation script, or any FastMCP client.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Running the Server](#running-the-server)
5. [Database Schema](#database-schema)
6. [Categories](#categories)
7. [Available MCP Tools](#available-mcp-tools)
8. [Development](#development)
9. [License](#license)

---

## Project Overview
The **Expense Tracker Remote MCP Server** is a Python project that demonstrates how to expose a domain‑specific service (expense tracking) via the **FastMCP** framework.  It provides a set of tools that can be invoked remotely to manage expenses, query data, and generate summaries.

## Features
- **Add, list, retrieve, update, and delete** expenses.
- **Search** expenses by keywords across category, sub‑category, merchant, and notes.
- **Summarize** spending by category within a date range.
- Compute **total spending** for a period.
- Serve a static **categories.json** file describing hierarchical expense categories.
- Simple SQLite backing store – no external database required.
- Input validation for dates (`YYYY‑MM‑DD`) and positive amounts.

---

## Installation
```bash
# Clone the repository (if not already done)
git clone <repo-url>
cd ExpenseTracker_RemoteMCPServer-main

# Create a virtual environment (Python >=3.10)
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt  # if a requirements file exists
# Or install directly
pip install "fastmcp>=3.4.4"
```

The project uses the following core files:
- [`server.py`](file:///c:/Users/adity/PycharmProjects/ExpenseTracker_RemoteMCPServer-main/server.py) – FastMCP server definition and tool implementations.
- [`database.py`](file:///c:/Users/adity/PycharmProjects/ExpenseTracker_RemoteMCPServer-main/database.py) – SQLite connection & initialization.
- [`utils.py`](file:///c:/Users/adity/PycharmProjects/ExpenseTracker_RemoteMCPServer-main/utils.py) – Simple validation helpers.
- [`categories.json`](file:///c:/Users/adity/PycharmProjects/ExpenseTracker_RemoteMCPServer-main/categories.json) – Hierarchical list of expense categories and sub‑categories.

---

## Running the Server
```bash
python server.py
```
The server will initialise the SQLite database (`expenses.db`) on first run and start listening on the default FastMCP address (`http://127.0.0.1:8000`).

You can now call any of the exposed tools via a FastMCP client.  For example, using the Python client:
```python
from fastmcp import FastMCPClient
client = FastMCPClient("http://127.0.0.1:8000")

# Add an expense
client.add_expense(
    date="2023-11-01",
    amount=45.60,
    category="food",
    subcategory="groceries",
    payment_method="credit_card",
    merchant="Supermart",
    note="Weekly groceries"
)
```

---

## Database Schema
The SQLite file **expenses.db** contains two tables defined in [`database.py`](file:///c:/Users/adity/PycharmProjects/ExpenseTracker_RemoteMCPServer-main/database.py):

| Table      | Columns |
|------------|---------|
| `expenses` | `id` (PK, auto), `date` (TEXT), `amount` (REAL &gt; 0), `category` (TEXT), `subcategory` (TEXT), `payment_method` (TEXT), `merchant` (TEXT), `note` (TEXT), `created_at` (TIMESTAMP) |
| `budgets`  | `id` (PK, auto), `month` (TEXT), `category` (TEXT), `budget` (REAL) |

The schema is created automatically by calling `init_db()` when the server starts.

---

## Categories
The hierarchical categories are stored in **categories.json**.  They are exposed via the MCP resource `expense://categories` and can be fetched with a client request.  Example excerpt:
```json
{
  "food": ["groceries", "dining_out", "coffee_tea"],
  "transport": ["fuel", "public_transport", "cab_ride_hailing"],
  ...
}
```
Full list: [`categories.json`](file:///c:/Users/adity/PycharmProjects/ExpenseTracker_RemoteMCPServer-main/categories.json).

---

## Available MCP Tools
| Tool | Description | Signature |
|------|-------------|-----------|
| `add_expense` | Insert a new expense record. | `add_expense(date: str, amount: float, category: str, subcategory: str = "", payment_method: str = "", merchant: str = "", note: str = "")` |
| `list_expenses` | Return all expenses between two dates. | `list_expenses(start_date: str, end_date: str)` |
| `get_expense` | Retrieve a single expense by its ID. | `get_expense(expense_id: int)` |
| `delete_expense` | Remove an expense by ID. | `delete_expense(expense_id: int)` |
| `update_expense` | Update fields of an existing expense. | `update_expense(expense_id: int, date: str, amount: float, category: str, subcategory: str = "", payment_method: str = "", merchant: str = "", note: str = "")` |
| `search_expenses` | Keyword search across category, sub‑category, merchant, and note. | `search_expenses(keyword: str)` |
| `summarize` | Aggregate total amounts per category for a date range. | `summarize(start_date: str, end_date: str)` |
| `total_spending` | Compute overall spending total for a date range. | `total_spending(start_date: str, end_date: str)` |
| `categories` (resource) | Returns the raw JSON of expense categories. | `categories()` |

All date arguments must follow the `YYYY‑MM‑DD` format; amounts must be positive numbers (validated by [`utils.py`](file:///c:/Users/adity/PycharmProjects/ExpenseTracker_RemoteMCPServer-main/utils.py)).

---

## Development
- **Testing**: Add unit tests under a `tests/` directory and run with `pytest`.
- **Linting**: Use `ruff` or `flake8` for style checks.
- **Database migrations**: For schema changes, modify `init_db()` and run a migration script that copies existing data to a new table.
- **Contributing**: Fork the repo, create a feature branch, and submit a pull request.

---

## License
This project is licensed under the MIT License – see the `LICENSE` file for details.

---


