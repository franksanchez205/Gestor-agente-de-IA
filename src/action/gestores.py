"""Marketplace de gestores verificados (invisible para el cliente).

El agente selecciona el gestor adecuado, le pasa el contexto y libera el pago
por escrow al completar el trámite.
"""

from dataclasses import dataclass


@dataclass
class Gestor:
    gestor_id: str
    name: str
    country: str
    specialties: list[str]
    verified: bool
    reputation_score: float  # 0-5
    cases_completed: int


class GestorMarketplace:
    def __init__(self, db):
        self.db = db

    async def find_best(self, country: str, tramite: str) -> Gestor | None:
        # Stub: selecciona el gestor con mejor reputación y disponibilidad
        return None

    async def assign(self, gestor_id: str, case_id: str, context: dict) -> None:
        # Stub: crea el caso para el gestor con todo el contexto
        pass

    async def release_payment(self, gestor_id: str, case_id: str) -> None:
        # Stub: libera el pago por escrow al completar
        pass