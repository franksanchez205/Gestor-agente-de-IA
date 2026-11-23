"""Modelos de datos (SQLAlchemy)."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    preferred_language = Column(String, default="es")
    preferred_channel = Column(String, default="whatsapp")
    created_at = Column(DateTime, default=datetime.utcnow)
    documents = relationship("Document", back_populates="user")
    cases = relationship("Case", back_populates="user")


class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    doc_type = Column(String, nullable=False)
    issued_by = Column(String, nullable=False)
    issued_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    credential = Column(JSON, nullable=True)  # W3C VC
    user = relationship("User", back_populates="documents")


class Case(Base):
    __tablename__ = "cases"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    tramite = Column(String, nullable=False)
    country = Column(String, nullable=False)
    status = Column(String, default="pending")
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    gestor_id = Column(String, nullable=True)
    user = relationship("User", back_populates="cases")