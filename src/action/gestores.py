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
    def __init__(self, db, session=None):
        self.db = db
        self.session = session

    async def find_best(self, country: str, tramite: str) -> Gestor | None:
        if self.session is None:
            # Stub: sin sesión de BD, no hay gestores registrados
            return None
        from src.data.models import Gestor as GestorModel
        from sqlalchemy import select
        stmt = (
            select(GestorModel)
            .where(GestorModel.country == country)
            .where(GestorModel.verified.is_(True))
            .order_by(GestorModel.reputation_score.desc())
        )
        result = self.session.execute(stmt).scalars().first()
        if result is None:
            return None
        return Gestor(
            gestor_id=result.id,
            name=result.name,
            country=result.country,
            specialties=result.specialties or [],
            verified=result.verified,
            reputation_score=result.reputation_score,
            cases_completed=result.cases_completed,
        )

    async def assign(self, gestor_id: str, case_id: str, context: dict) -> None:
        # Crea el caso para el gestor con todo el contexto (invisible para el cliente)
        pass

    async def release_payment(self, gestor_id: str, case_id: str) -> None:
        # Libera el pago por escrow al completar el trámite
        pass