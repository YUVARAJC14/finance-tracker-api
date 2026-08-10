from fastapi import FastAPI

expenses = []


def add_expense(amount, category):
    expense = {"amount": amount, "category": category}
    expenses.append(expense)
    print(f"Added {amount} to {category}")

def view_expenses():
    for i, e in enumerate(expenses):
        print(f"{i}: {e['amount']} - {e['category']}")

def total_by_category(category):
    total = 0
    for e in expenses:
        if e["category"] == category:
            total += e["amount"]
    return total

def delete_expense(index):
    if 0 <= index < len(expenses):
        removed = expenses.pop(index)
        print(f"Removed {removed['amount']} from {removed['category']}")
    else:
        print("Invalid index")

app = FastAPI()

@app.post("/expenses")
def create_expense(amount: float, category: str):
    add_expense(amount, category)
    return {"message": "Expense added", "data": expenses[-1]}

@app.get("/expenses")
def get_expenses():
    return expenses

@app.get("/expenses/total/{category}")
def get_total(category: str):
    return {"category": category, "total": total_by_category(category)}

@app.delete("/expenses/{index}")
def remove_expense(index: int):
    delete_expense(index)
    return {"message": f"Deleted expense at index {index}"}
