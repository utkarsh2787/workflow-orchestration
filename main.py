from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
from app.create_table import create_tables
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import engine, get_db, Base
import uvicorn
from app.api.v1 import workflow, user, tasks


# Create FastAPI application
app = FastAPI(
    title="Workflow Orchestration API",
    description="A workflow orchestration system with MySQL database",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",      # for local Next.js dev
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] to allow all (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],            # allow all HTTP methods
    allow_headers=["*"],            # allow all headers
)
# Create database tables
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    # create_tables()
    print("Database tables created successfully!")


app.include_router(user.router)
app.include_router(workflow.router)
app.include_router(tasks.router)


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "Workflow Orchestration API is running!", "status": "healthy"}


# Database connection test endpoint
@app.get("/health/db")
async def check_database_connection(db: Session = Depends(get_db)):
    """Test database connectivity"""
    try:
        # Execute a simple query to test connection
        result = db.execute(text("SELECT 1 as test"))
        test_value = result.scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "test_query_result": test_value,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )


# Entry point for running the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True, log_level="info")
