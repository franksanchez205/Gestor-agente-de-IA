"""Tests unitarios de la capa de acción — portales."""

import pytest
from src.action.portals import PortalClient, PortalResult


@pytest.mark.asyncio
async def test_submit_form_returns_result():
    client = PortalClient(base_url="https://portal.example.com", credentials={"token": "abc"})
    result = await client.submit_form(
        form_data={"name": "Juan"},
        documents=[{"doc_type": "passport"}],
    )
    assert isinstance(result, PortalResult)
    assert result.success is True
    assert result.tramite_number is not None


@pytest.mark.asyncio
async def test_check_status_returns_string():
    client = PortalClient(base_url="https://portal.example.com", credentials={"token": "abc"})
    status = await client.check_status("TRM-001")
    assert isinstance(status, str)
    assert len(status) > 0