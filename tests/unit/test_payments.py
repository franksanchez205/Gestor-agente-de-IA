"""Tests unitarios de la capa de acción — pagos."""

import pytest
from src.action.payments import PaymentClient, PaymentResult


@pytest.mark.asyncio
async def test_pay_fee_returns_result():
    client = PaymentClient(provider="stripe", tokenized_card="tok_abc")
    result = await client.pay_fee(amount=50.0, currency="USD", tramite_number="TRM-001")
    assert isinstance(result, PaymentResult)
    assert result.success is True
    assert result.transaction_id is not None
    assert result.amount == 50.0
    assert result.currency == "USD"