from datetime import datetime


def validate_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be YYYY-MM-DD")


def validate_amount(amount):
    amount = float(amount)

    if amount <= 0:
        raise ValueError("Amount must be positive.")

    return amount