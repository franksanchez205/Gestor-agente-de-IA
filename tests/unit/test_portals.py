"""Tests unitarios de la capa de acción — portales."""

import pytest
from src.action.portals import PortalClient, PortalResult, PortalClientFactory


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


def test_portal_client_factory_supported_countries():
    factory = PortalClientFactory(configs={
        "AR": {"base_url": "https://ar.example.com", "credentials": {"token": "ar"}},
        "ES": {"base_url": "https://es.example.com", "credentials": {"token": "es"}},
    })
    assert set(factory.supported_countries()) == {"AR", "ES"}


def test_portal_client_factory_get_client():
    factory = PortalClientFactory(configs={
        "AR": {"base_url": "https://ar.example.com", "credentials": {"token": "ar"}},
    })
    client = factory.get_client("AR")
    assert client.country == "AR"
    assert client.base_url == "https://ar.example.com"


def test_portal_client_factory_unknown_country_raises():
    factory = PortalClientFactory(configs={})
    with pytest.raises(ValueError):
        factory.get_client("XX")