"""Tests unitarios del marketplace de gestores (con BD)."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data.models import Base, Gestor
from src.action.gestores import GestorMarketplace


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


@pytest.mark.asyncio
async def test_find_best_returns_verified_gestor(session):
    g1 = Gestor(id="g1", name="Ana", country="AR", verified=True, reputation_score=4.5, cases_completed=10)
    g2 = Gestor(id="g2", name="Luis", country="AR", verified=False, reputation_score=4.9, cases_completed=20)
    session.add_all([g1, g2])
    session.commit()

    marketplace = GestorMarketplace(db=None, session=session)
    result = await marketplace.find_best(country="AR", tramite="renovacion")
    assert result is not None
    assert result.gestor_id == "g1"  # verified, highest reputation among verified


@pytest.mark.asyncio
async def test_find_best_returns_none_when_no_verified(session):
    g = Gestor(id="g1", name="Ana", country="AR", verified=False, reputation_score=4.5, cases_completed=10)
    session.add(g)
    session.commit()

    marketplace = GestorMarketplace(db=None, session=session)
    result = await marketplace.find_best(country="AR", tramite="renovacion")
    assert result is None


@pytest.mark.asyncio
async def test_find_best_filters_by_country(session):
    g1 = Gestor(id="g1", name="Ana", country="AR", verified=True, reputation_score=4.5, cases_completed=10)
    g2 = Gestor(id="g2", name="Pedro", country="ES", verified=True, reputation_score=4.9, cases_completed=20)
    session.add_all([g1, g2])
    session.commit()

    marketplace = GestorMarketplace(db=None, session=session)
    result = await marketplace.find_best(country="ES", tramite="apostilla")
    assert result is not None
    assert result.gestor_id == "g2"