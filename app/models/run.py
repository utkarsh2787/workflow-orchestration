from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    status = Column(String(50), default="running")
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)

    workflow = relationship("Workflow", back_populates="runs")
    logs = relationship("Log", back_populates="run")
