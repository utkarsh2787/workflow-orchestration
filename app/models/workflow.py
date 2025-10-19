from app.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    status = Column(String(50), default="draft")
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", back_populates="workflows")
    tasks = relationship("Task", back_populates="workflow")
    runs = relationship("Run", back_populates="workflow")


def create_workflow(session, name: str, description: str | None = None, created_by: int | None = None, status: str = "draft") -> Workflow:
    """Create and persist a Workflow."""
    wf = Workflow(name=name, description=description, created_by=created_by, status=status)
    session.add(wf)
    session.commit()
    session.refresh(wf)
    return wf