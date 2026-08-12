from fastapi import FastAPI
from database import get_session, init_db, Expense
from sqlalchemy import func
from pydantic import BaseModel, Field
import datetime
import os
from dotenv import load_dotenv
from typing import Optional
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
    session = get_session()
    expense = Expense(amount=amount, category=category, date=expense_date)
    session.add(expense)
    session.commit()
    session.refresh(expense)
    result = {"id": expense.id, "amount": expense.amount, "category": expense.category, "date": str(expense.date)}
    session.close()
    return result

def view_expenses(limit=10, offset=0, category=None):
    session = get_session()
    query = session.query(Expense)
    if category:
        query = query.filter(Expense.category == category)
    rows = query.limit(limit).offset(offset).all()
    result = [{"id": r.id, "amount": r.amount, "category": r.category, "date": str(r.date)} for r in rows]
    session.close()
    return result

def total_by_category(category):
    session = get_session()
    total = session.query(func.sum(Expense.amount)).filter(Expense.category == category).scalar()
    session.close()
    return total or 0

def delete_expense(expense_id):
    session = get_session()
    expense = session.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()
    session.close()

def total_by_month():
    session = get_session()
    rows = session.query(
        func.strftime('%Y-%m', Expense.date).label('month'),
        func.sum(Expense.amount).label('total')
    ).group_by('month').order_by('month').all()
    session.close()
    return [{"month": r.month, "total": r.total} for r in rows]

def total_by_category_and_month():
    session = get_session()
    rows = session.query(
        func.strftime('%Y-%m', Expense.date).label('month'),
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).group_by('month', Expense.category).order_by('month', Expense.category).all()
    session.close()
    return [{"month": r.month, "category": r.category, "total": r.total} for r in rows]

app = FastAPI()

@app.post("/expenses", dependencies=[Depends(verify_api_key)])
def create_expense(expense: ExpenseCreate):
    result = add_expense(expense.amount, expense.category, expense.date)
    return {"message": "Expense added", "data": result}

@app.get("/expenses")
def get_expenses(limit: int = 10, offset: int = 0, category: Optional[str] = None):
    return view_expenses(limit=limit, offset=offset, category=category)

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
