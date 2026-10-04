# 💸 Expense Tracker MCP Server

![FastMCP](https://img.shields.io/badge/FastMCP-Ready-blue)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)
![Status](https://img.shields.io/badge/Status-Live-success)

A robust, lightweight **FastMCP** server that provides a complete API for personal expense and budget tracking. This server adheres to the Model Context Protocol (MCP), allowing AI agents (like Claude, ChatGPT) and automated scripts to securely manage expenses, check budgets, and generate spending analytics.

---

## 🚀 Live Deployment

The server is currently **deployed and publicly accessible**. Any MCP-compatible client or connector can interact with it using the following endpoint:

**🔗 Connection URL:**  
`https://distinctive-apricot-pelican.fastmcp.app/mcp`

### Connecting via Claude Desktop (Example)
You can configure Claude Desktop to use this remote MCP server by adding an HTTP connector to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "expense_tracker": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/inspector", "https://distinctive-apricot-pelican.fastmcp.app/mcp"]
    }
  }
}
```
*(Note: adjust connector args based on your specific client implementation for remote HTTP MCP endpoints).*

### Connecting via Python
```python
from fastmcp import FastMCPClient

client = FastMCPClient("https://distinctive-apricot-pelican.fastmcp.app/mcp")

# Example: Check remaining food budget for the month
result = client.check_budget(month="2026-10", category="food")
print(result)
```

---

## ✨ Key Features

- **Expense Management**: Add, update, delete, and list expenses with robust validation.
- **Budgeting (New!)**: Set monthly budgets by category and instantly check remaining balances.
- **Smart Search**: Search expenses by keywords across categories, merchants, and notes.
- **Spending Analytics**: Summarize expenses by category and calculate total spending over date ranges.
- **Strict Validation**: Enforces valid categories (via `categories.json`), strictly positive amounts, and correct date formats (`YYYY-MM-DD`).
- **Resilient**: Built-in SQLite context managers and structured error handling prevent crashes and return clear agentic feedback.

---

## 🛠️ Available MCP Tools

| Tool | Description | Signature |
|------|-------------|-----------|
| `add_expense` | Insert a new expense record. | `add_expense(date: str, amount: float, category: str, subcategory: str = "", ...)` |
| `list_expenses` | Return all expenses between two dates. | `list_expenses(start_date: str, end_date: str)` |
| `get_expense` | Retrieve a single expense by its ID. | `get_expense(expense_id: int)` |
| `update_expense` | Update fields of an existing expense. | `update_expense(expense_id: int, date: str, amount: float, category: str, ...)` |
| `delete_expense` | Remove an expense by ID. | `delete_expense(expense_id: int)` |
| `search_expenses` | Keyword search across category, merchant, and note. | `search_expenses(keyword: str)` |
| `summarize` | Aggregate total amounts per category for a date range. | `summarize(start_date: str, end_date: str)` |
| `total_spending` | Compute overall spending total for a date range. | `total_spending(start_date: str, end_date: str)` |
| `set_budget` | **[NEW]** Set a spending limit for a specific month/category. | `set_budget(month: str, category: str, budget: float)` |
| `get_budgets` | **[NEW]** List all budgets for a given month (YYYY-MM). | `get_budgets(month: str)` |
| `check_budget` | **[NEW]** Compare actual spending vs budget for a month/category. | `check_budget(month: str, category: str)` |

### 📂 Resources
- `expense://categories` — Returns the full hierarchical JSON of valid expense categories and sub-categories.

---

## 💻 Local Development

If you'd like to run the server locally, contribute, or modify the codebase:

```bash
# 1. Clone the repository
git clone https://github.com/adityakes11/ExpenseTracker_RemoteMCPServer.git
cd ExpenseTracker_RemoteMCPServer

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install "fastmcp>=3.4.4"

# 4. Start the server
python server.py
```
The local server will automatically initialize an SQLite database (`expenses.db`) and listen on `http://127.0.0.1:8000`.

---

## 📄 License
This project is licensed under the MIT License.
