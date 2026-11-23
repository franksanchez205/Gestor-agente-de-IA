"""Tests unitarios de notificaciones proactivas."""

import pytest
from datetime import datetime, timedelta
from src.agent.memory import PersonalMemory, UserProfile, Document
from src.agent.notifications import NotificationService


class FakeMessenger:
    def __init__(self):
        self.messages = []

    async def send(self, text: str):
        self.messages.append(text)


@pytest.fixture
def memory():
    profile = UserProfile(user_id="u1", name="Juan", nationality="AR")
    mem = PersonalMemory(profile=profile)
    soon = datetime.utcnow() + timedelta(days=30)
    mem.add_document(Document(doc_id="d1", doc_type="permit", issued_by="AR", issued_at=datetime.utcnow(), expires_at=soon))
    return mem


@pytest.mark.asyncio
async def test_check_expiring_documents_sends_message(memory):
    messenger = FakeMessenger()
    service = NotificationService(messenger=messenger)
    await service.check_expiring_documents(memory, days_ahead=60)
    assert len(messenger.messages) == 1
    assert "vence" in messenger.messages[0]


@pytest.mark.asyncio
async def test_check_expiring_documents_none_when_not_expiring():
    profile = UserProfile(user_id="u2", name="Ana", nationality="ES")
    mem = PersonalMemory(profile=profile)
    messenger = FakeMessenger()
    service = NotificationService(messenger=messenger)
    await service.check_expiring_documents(mem, days_ahead=60)
    assert len(messenger.messages) == 0


@pytest.mark.asyncio
async def test_remind_appointment_sends_message():
    messenger = FakeMessenger()
    service = NotificationService(messenger=messenger)
    await service.remind_appointment({"time": "09:00", "location": "Migraciones"}, hours_before=24)
    assert len(messenger.messages) == 1
    assert "Recordatorio" in messenger.messages[0]