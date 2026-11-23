"""Agenda de citas (presenciales o virtuales) y recordatorios."""

from datetime import datetime


class AppointmentService:
    def __init__(self, calendar_client):
        self.calendar = calendar_client

    async def schedule(self, user_id: str, when: datetime, location: str, tramite: str) -> dict:
        event = await self.calendar.create_event(
            title=f"Cita: {tramite}",
            start=when,
            location=location,
            reminder_minutes=24 * 60,
        )
        return {"event_id": event["id"], "when": when, "location": location}

    async def reschedule(self, event_id: str, new_when: datetime) -> dict:
        return await self.calendar.update_event(event_id, start=new_when)