"""
A simple inventory management system script.

This module provides functions to add, remove, load, save,
and report on items in an inventory.
"""
import json
import logging
from datetime import datetime

# --- Logging Configuration ---
# Fix: Added basic logging configuration to use the imported module.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds an item and its quantity to the inventory.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to add.
        qty (int): The quantity to add.
        logs (list, optional): A list to append log messages to.
    """
    # Fix 1: Resolved "dangerous-default-value" (Pylint W0102).
    if logs is None:
        logs = []

    if not item or not isinstance(qty, int):
        logging.error("Invalid item name or quantity type provided.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty

    # Fix 2: Used an f-string as suggested by Pylint (C0209).
    log_message = f"Added {qty} of {item}"
    logs.append(f"{datetime.now()}: {log_message}")
    logging.info(log_message)


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the inventory.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    try:
        if stock_data[item] > qty:
            stock_data[item] -= qty
        else:
            del stock_data[item]
    # Fix 3: Replaced bare 'except' with a specific exception (KeyError).
    except KeyError:
        # Fix 4: Broke long line (C0301)
        logging.warning(
            "Attempted to remove '%s', which is not in the inventory.",
            item
        )
        # Fix 5: Removed "unnecessary-pass" (W0107).


def get_qty(stock_data, item):
    """
    Gets the quantity of a specific item.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to query.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads inventory data from a JSON file.

    Args:
        file (str): The name of the JSON file to load from.

    Returns:
        dict: The loaded inventory data.
    """
    try:
        # Fix 6: Used 'with' statement for safer file handling.
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(
            "Inventory file not found. Starting with an empty inventory."
        )
        return {}
    except json.JSONDecodeError:
        logging.error("Could not decode JSON from the inventory file.")
        return {}


def save_data(stock_data, file="inventory.json"):
    """
    Saves the current inventory data to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str): The name of the JSON file to save to.
    """
    # Fix 6: Used 'with' statement for safer file handling.
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)


def print_data(stock_data):
    """
    Prints a formatted report of all items in the inventory.

    Args:
        stock_data (dict): The inventory dictionary to print.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    """
    Returns a list of items with stock below a given threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int): The stock level to check against.

    Returns:
        list: A list of item names below the threshold.
    """
    return [
        item for item, quantity in stock_data.items()
        if quantity < threshold
    ]


def main():
    """Main function to run the inventory system logic."""

    # Fix 7: Removed "global-statement" (W0603).
    # 'stock_data' is now a local variable in 'main' that is
    # passed as an argument to all other functions.
    stock_data = load_data()

    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", 20)
    add_item(stock_data, 123, "ten")  # Invalid types are now handled
    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)  # Non-existent item is handled

    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items: {check_low_items(stock_data)}")

    print_data(stock_data)
    save_data(stock_data)

    # Fix 8: Removed the dangerous 'eval' call.
    logging.info("Script finished.")


if __name__ == "__main__":
    main()
