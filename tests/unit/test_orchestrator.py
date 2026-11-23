"""Tests unitarios del orquestador de acciones."""

import pytest
from src.agent.orchestrator import Orchestrator, TramitePlan, PlanStep, StepStatus


@pytest.mark.asyncio
async def test_runs_steps_without_confirmation():
    async def confirm(msg):
        return True

    orch = Orchestrator(confirm_callback=confirm)
    plan = TramitePlan(plan_id="p1", tramite="renovacion", country="AR")
    plan.steps = [
        PlanStep(step_id="s1", description="Llenar formulario", action=None, requires_confirmation=False),
        PlanStep(step_id="s2", description="Pagar tasa", action=None, requires_confirmation=False),
    ]

    result = await orch.run(plan)
    assert result.is_complete
    assert all(s.status == StepStatus.DONE for s in result.steps)


@pytest.mark.asyncio
async def test_stops_when_confirmation_rejected():
    async def confirm(msg):
        return False

    orch = Orchestrator(confirm_callback=confirm)
    plan = TramitePlan(plan_id="p2", tramite="renovacion", country="AR")
    plan.steps = [
        PlanStep(step_id="s1", description="Enviar documentos", action=None, requires_confirmation=True),
    ]

    result = await orch.run(plan)
    assert not result.is_complete
    assert result.steps[0].status == StepStatus.FAILED


@pytest.mark.asyncio
async def test_action_failure_marks_step_failed():
    async def action():
        raise RuntimeError("portal caido")

    async def confirm(msg):
        return True

    orch = Orchestrator(confirm_callback=confirm)
    plan = TramitePlan(plan_id="p3", tramite="renovacion", country="AR")
    plan.steps = [
        PlanStep(step_id="s1", description="Enviar al portal", action=action, requires_confirmation=False),
    ]

    result = await orch.run(plan)
    assert not result.is_complete
    assert result.steps[0].status == StepStatus.FAILED
    assert "portal caido" in result.steps[0].result["error"]


@pytest.mark.asyncio
async def test_action_success_stores_result():
    async def action():
        return {"tramite_number": "TRM-001"}

    async def confirm(msg):
        return True

    orch = Orchestrator(confirm_callback=confirm)
    plan = TramitePlan(plan_id="p4", tramite="renovacion", country="AR")
    plan.steps = [
        PlanStep(step_id="s1", description="Enviar", action=action, requires_confirmation=False),
    ]

    result = await orch.run(plan)
    assert result.is_complete
    assert result.steps[0].result == {"tramite_number": "TRM-001"}