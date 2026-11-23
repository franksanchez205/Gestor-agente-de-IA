"""Memoria personal del agente (Jarvis-style).

El cliente nunca repite información. El agente recuerda perfil, expediente,
historial, contexto activo y preferencias entre sesiones.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class UserProfile:
    user_id: str
    name: str
    nationality: str
    countries_of_interest: list[str] = field(default_factory=list)
    preferred_language: str = "es"
    preferred_tone: str = "cercano"  # formal | cercano | directo
    preferred_channel: str = "whatsapp"  # whatsapp | voice | app
    notification_hours: tuple[int, int] = (8, 20)


@dataclass
class Document:
    doc_id: str
    doc_type: str  # passport, title, apostille, permit, ...
    issued_by: str
    issued_at: datetime
    expires_at: datetime | None = None
    credential: dict[str, Any] | None = None  # W3C Verifiable Credential


@dataclass
class CaseHistory:
    case_id: str
    tramite: str
    country: str
    started_at: datetime
    completed_at: datetime | None = None
    outcome: str | None = None  # approved | rejected | pending
    gestor_id: str | None = None


@dataclass
class PersonalMemory:
    """Memoria personal persistente del cliente."""

    profile: UserProfile
    documents: list[Document] = field(default_factory=list)
    history: list[CaseHistory] = field(default_factory=list)
    active_context: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)

    def add_document(self, doc: Document) -> None:
        self.documents.append(doc)

    def expiring_soon(self, days: int = 60) -> list[Document]:
        now = datetime.utcnow()
        return [
            d for d in self.documents
            if d.expires_at is not None
            and (d.expires_at - now).days <= days
        ]

    def to_prompt_context(self) -> str:
        """Serializa la memoria para inyectarla en el prompt del LLM."""
        lines = [f"Cliente: {self.profile.name} ({self.profile.nationality})"]
        lines.append(f"Países de interés: {', '.join(self.profile.countries_of_interest)}")
        lines.append(f"Canal preferido: {self.profile.preferred_channel}")
        lines.append(f"Documentos: {len(self.documents)}")
        for d in self.documents:
            exp = d.expires_at.strftime("%Y-%m-%d") if d.expires_at else "sin vencimiento"
            lines.append(f"  - {d.doc_type} ({d.issued_by}) vence {exp}")
        if self.active_context:
            lines.append(f"Contexto activo: {self.active_context}")
        return "\n".join(lines)