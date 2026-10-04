from datetime import datetime
import json
import os

BASE_DIR = os.path.dirname(__file__)
CATEGORY_PATH = os.path.join(BASE_DIR, "categories.json")

# Load valid categories into memory for validation
with open(CATEGORY_PATH, "r", encoding="utf-8") as f:
    VALID_CATEGORIES = json.load(f)


def validate_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be YYYY-MM-DD")


def validate_amount(amount):
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")

    if amount <= 0:
        raise ValueError("Amount must be positive.")

    return amount


def validate_category(category: str, subcategory: str = ""):
    """Validates that the category and subcategory exist in categories.json"""
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category: '{category}'. Valid categories are keys in categories.json.")
    
    if subcategory and subcategory not in VALID_CATEGORIES[category]:
        raise ValueError(f"Invalid subcategory '{subcategory}' for category '{category}'.")