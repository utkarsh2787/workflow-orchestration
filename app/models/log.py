
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    message = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)

    run = relationship("Run", back_populates="logs")
    task = relationship("Task", back_populates="logs")


def create_log(session, run_id: int, task_id: int, message: str) -> Log:
    """Create a new log entry."""
    new_log = Log(run_id=run_id, task_id=task_id, message=message)
    session.add(new_log)
    session.commit()
    session.refresh(new_log)
    return new_log