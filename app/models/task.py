from datetime import datetime
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    command = Column(String(500))  # what to run
    order = Column(Integer)
    status = Column(String(50), default="pending")
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(String(200), nullable=False)
    config = Column(JSON, nullable=True)
    inputs = Column(JSON, nullable=True)
    outputs = Column(JSON, nullable=True)

    workflow = relationship("Workflow", back_populates="tasks")
    logs = relationship("Log", back_populates="task")