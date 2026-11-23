"""Pagos de tasas oficiales (tokenizados, con confirmación humana)."""

from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    transaction_id: str | None = None
    amount: float = 0.0
    currency: str = "USD"
    receipt: dict | None = None


class PaymentClient:
    def __init__(self, provider: str, tokenized_card: str):
        self.provider = provider
        self.tokenized_card = tokenized_card

    async def pay_fee(self, amount: float, currency: str, tramite_number: str) -> PaymentResult:
        # Stub: en producción usa pasarela de pago (Stripe, etc.)
        return PaymentResult(success=True, transaction_id="TXN-0001", amount=amount, currency=currency)