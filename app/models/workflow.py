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