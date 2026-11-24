"""Tests unitarios de exportación/eliminación de datos del usuario."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import Base, User, Document, Case
from src.credentials.data_export import DataExporter


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


def test_export_user_data(session):
    user = User(id="u1", name="Juan", nationality="AR")
    session.add(user)
    session.add(Document(id="d1", user_id="u1", doc_type="passport", issued_by="AR", issued_at=__import__("datetime").datetime.utcnow()))
    session.add(Case(id="c1", user_id="u1", tramite="renovacion", country="AR"))
    session.commit()

    exporter = DataExporter(session=session)
    data = exporter.export_user_data("u1")
    assert data["profile"]["name"] == "Juan"
    assert len(data["documents"]) == 1
    assert len(data["cases"]) == 1


def test_export_unknown_user_returns_empty(session):
    exporter = DataExporter(session=session)
    data = exporter.export_user_data("unknown")
    assert data == {}


def test_delete_user_data(session):
    user = User(id="u1", name="Juan", nationality="AR")
    session.add(user)
    session.add(Document(id="d1", user_id="u1", doc_type="passport", issued_by="AR", issued_at=__import__("datetime").datetime.utcnow()))
    session.commit()

    exporter = DataExporter(session=session)
    assert exporter.delete_user_data("u1") is True
    assert session.query(User).filter(User.id == "u1").first() is None
    assert session.query(Document).filter(Document.user_id == "u1").count() == 0