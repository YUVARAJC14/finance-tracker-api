from fastapi import FastAPI
from database import get_connection, init_db
from pydantic import BaseModel, Field
import datetime
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Header

load_dotenv()

API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0, description="Amount must be greater than 0")
    category: str = Field(min_length=1, description="Category cannot be empty")
    date: datetime.date = Field(default_factory=datetime.date.today, description="Date of expense")

expenses = []

init_db()

def add_expense(amount, category, expense_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, str(expense_date))
    )
    conn.commit()
    conn.close()

def view_expenses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return [dict(row) for row in rows]

def total_by_category(category):
    conn = get_connection()
    result = conn.execute(
        "SELECT SUM(amount) as total FROM expenses WHERE category = ?", (category,)
    ).fetchone()
    conn.close()
    return result["total"] or 0

def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def total_by_month():
    conn = get_connection()
    rows = conn.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        GROUP BY month
        ORDER BY month
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def total_by_category_and_month():
    conn = get_connection()
    rows = conn.execute("""
        SELECT strftime('%Y-%m', date) as month, category, SUM(amount) as total
        FROM expenses
        GROUP BY month, category
        ORDER BY month, category
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

app = FastAPI()

@app.post("/expenses", dependencies=[Depends(verify_api_key)])
def create_expense(expense: ExpenseCreate):
    add_expense(expense.amount, expense.category, expense.date)
    all_expenses = view_expenses()
    return {"message": "Expense added", "data": all_expenses[-1]}

@app.get("/expenses")
def get_expenses():
    return view_expenses()

@app.get("/expenses/total/{category}")
def get_total(category: str):
    return {"category": category, "total": total_by_category(category)}

@app.delete("/expenses/{index}", dependencies=[Depends(verify_api_key)])
def remove_expense(index: int):
    delete_expense(index)
    return {"message": f"Deleted expense at index {index}"}

@app.get("/expenses/summary/monthly")
def get_monthly_summary():
    return total_by_month()

@app.get("/expenses/summary/monthly-category")
def get_monthly_category_summary():
    return total_by_category_and_month()
