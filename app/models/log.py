
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
