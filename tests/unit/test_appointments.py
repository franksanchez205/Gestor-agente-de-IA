"""Tests unitarios de agenda de citas."""

import pytest
from datetime import datetime
from src.action.appointments import AppointmentService


class FakeCalendar:
    def __init__(self):
        self.events = []

    async def create_event(self, title, start, location, reminder_minutes):
        ev = {"id": f"ev-{len(self.events)+1}", "title": title, "start": start, "location": location}
        self.events.append(ev)
        return ev

    async def update_event(self, event_id, start):
        return {"id": event_id, "start": start}


@pytest.mark.asyncio
async def test_schedule_creates_event():
    cal = FakeCalendar()
    service = AppointmentService(calendar_client=cal)
    when = datetime(2026, 12, 1, 9, 0)
    result = await service.schedule(user_id="u1", when=when, location="Migraciones", tramite="renovacion")
    assert result["event_id"] == "ev-1"
    assert result["location"] == "Migraciones"
    assert len(cal.events) == 1


@pytest.mark.asyncio
async def test_reschedule_updates_event():
    cal = FakeCalendar()
    service = AppointmentService(calendar_client=cal)
    new_when = datetime(2026, 12, 2, 10, 0)
    result = await service.reschedule(event_id="ev-1", new_when=new_when)
    assert result["id"] == "ev-1"
    assert result["start"] == new_when