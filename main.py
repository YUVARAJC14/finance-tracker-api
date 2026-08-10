expenses = []


def add_expense(amount, category):
    expense = {"amount": amount, "category": category}
    expenses.append(expense)
    print(f"Added {amount} to {category}")


add_expense(500, "food")
add_expense(1200, "travel")
print(expenses)
