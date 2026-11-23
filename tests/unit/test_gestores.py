"""Tests unitarios del marketplace de gestores."""

import pytest
from src.action.gestores import GestorMarketplace, Gestor


class FakeDB:
    pass


@pytest.mark.asyncio
async def test_find_best_returns_none_when_empty():
    marketplace = GestorMarketplace(db=FakeDB())
    result = await marketplace.find_best(country="AR", tramite="renovacion")
    assert result is None


@pytest.mark.asyncio
async def test_assign_and_release_payment_do_not_raise():
    marketplace = GestorMarketplace(db=FakeDB())
    await marketplace.assign(gestor_id="g1", case_id="c1", context={"tramite": "renovacion"})
    await marketplace.release_payment(gestor_id="g1", case_id="c1")