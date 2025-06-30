# FastAPI Starter Project

## Setup

1. Create a virtual environment and activate it
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Set up your PostgreSQL database and update `.env`
4. Run the app:
```
uvicorn main:app --reload
```
5. Run "python -c "from app.models import Base; from app.database import engine; Base.metadata.create_all(bind=engine)""
6. Setup environment and run "uvicorn app.main:app --reload"