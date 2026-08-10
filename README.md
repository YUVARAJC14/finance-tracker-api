# Personal Finance Tracker API

A REST API built with FastAPI and SQLite to track income and expenses, view totals by category, and manage entries.

## Tech Stack
- Python
- FastAPI
- SQLite
- Uvicorn

## Features
- Add an expense (amount + category)
- View all expenses
- Get total spending by category
- Delete an expense by ID
- Data persists in a local SQLite database

## Running Locally
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

Then open http://127.0.0.1:8000/docs to try the API.

## What I learned
Building this taught me how to design REST endpoints, connect a FastAPI app to a SQLite database safely (parameterized queries), and structure a Python project properly with a virtual environment and version control.
