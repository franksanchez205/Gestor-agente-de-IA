"""Notificaciones proactivas del agente.

Avisa con anticipación sobre vencimientos, cambios normativos y citas.
"""

from datetime import datetime, timedelta


class NotificationService:
    def __init__(self, messenger):
        self.messenger = messenger

    async def check_expiring_documents(self, memory, days_ahead: int = 60) -> None:
        for doc in memory.expiring_soon(days_ahead):
            remaining = (doc.expires_at - datetime.utcnow()).days
            await self.messenger.send(
                f"Tu {doc.doc_type} vence en {remaining} días "
                f"({doc.expires_at.strftime('%d/%m/%Y')}). "
                f"¿Querés que gestione la renovación?"
            )

    async def remind_appointment(self, appointment: dict, hours_before: int = 24) -> None:
        await self.messenger.send(
            f"Recordatorio: tenés cita mañana a las {appointment['time']} "
            f"en {appointment['location']}. ¿Querés que te envíe la ubicación?"
        )