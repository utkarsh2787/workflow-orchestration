from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import engine, get_db, Base
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="Workflow Orchestration API",
    description="A workflow orchestration system with MySQL database",
    version="1.0.0"
)

# Create database tables
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

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
            "test_query_result": test_value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Entry point for running the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
