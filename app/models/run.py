from datetime import datetime
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    status = Column(String(50), default="running")
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    inputs = Column(JSON, nullable=True)
    outputs = Column(JSON, nullable=True)
    workflow = relationship("Workflow", back_populates="runs")
    logs = relationship("Log", back_populates="run")


def create_run(session, workflow_id, status, inputs)->Run:
    run = Run(workflow_id=workflow_id, status=status, inputs=inputs)
    session.add(run)
    session.commit()
    session.refresh(run)
    return run