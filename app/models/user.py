from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    workflows = relationship("Workflow", back_populates="creator")


def create_user(session, name: str, email: str) -> User:
    """Create and persist a User."""
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
