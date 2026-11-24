"""Modelos de datos (SQLAlchemy)."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    preferred_language = Column(String, default="es")
    preferred_channel = Column(String, default="whatsapp")
    org_id = Column(String, ForeignKey("organizations.id"), nullable=True)
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
    title = Column(String, nullable=True)
    tramite = Column(String, nullable=False)
    country = Column(String, nullable=False)
    status = Column(String, default="pending")
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    gestor_id = Column(String, nullable=True)
    user = relationship("User", back_populates="cases")


class Gestor(Base):
    __tablename__ = "gestores"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    specialties = Column(JSON, nullable=True)
    verified = Column(Boolean, default=False)
    reputation_score = Column(Float, default=0.0)
    cases_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    gestor_id = Column(String, ForeignKey("gestores.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    status = Column(String, nullable=False, default="pending")  # pending | released | refunded
    created_at = Column(DateTime, default=datetime.utcnow)
    released_at = Column(DateTime, nullable=True)


class Credential(Base):
    __tablename__ = "credentials"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    doc_id = Column(String, ForeignKey("documents.id"), nullable=True)
    vc_jwt = Column(String, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    revoked = Column(Boolean, default=False)


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    org_type = Column(String, nullable=False)  # ong | organism
    contact_email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    cupos = relationship("Cupo", back_populates="organization")


class Cupo(Base):
    __tablename__ = "cupos"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    beneficiary_email = Column(String, nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    organization = relationship("Organization", back_populates="cupos")