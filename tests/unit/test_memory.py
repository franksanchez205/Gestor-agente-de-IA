"""Tests unitarios de la memoria personal."""

import pytest
from datetime import datetime, timedelta
from src.agent.memory import PersonalMemory, UserProfile, Document


@pytest.fixture
def memory():
    profile = UserProfile(user_id="u1", name="Juan", nationality="AR", countries_of_interest=["AR", "ES"])
    return PersonalMemory(profile=profile)


def test_add_document(memory):
    doc = Document(doc_id="d1", doc_type="passport", issued_by="AR", issued_at=datetime.utcnow())
    memory.add_document(doc)
    assert len(memory.documents) == 1


def test_expiring_soon(memory):
    soon = datetime.utcnow() + timedelta(days=30)
    doc = Document(doc_id="d2", doc_type="permit", issued_by="AR", issued_at=datetime.utcnow(), expires_at=soon)
    memory.add_document(doc)
    assert len(memory.expiring_soon(60)) == 1
    assert len(memory.expiring_soon(10)) == 0


def test_to_prompt_context(memory):
    ctx = memory.to_prompt_context()
    assert "Juan" in ctx