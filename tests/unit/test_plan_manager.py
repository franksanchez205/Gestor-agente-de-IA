"""Tests unitarios del gestor de planes múltiples (V2)."""

import pytest
from src.agent.orchestrator import PlanManager, TramitePlan, PlanStep


def test_add_and_get_plans():
    pm = PlanManager()
    plan = TramitePlan(plan_id="p1", tramite="renovacion", country="AR")
    pm.add_plan("u1", plan)
    assert len(pm.get_plans("u1")) == 1
    assert pm.get_plan("u1", "p1") is plan


def test_get_active_plans_excludes_completed():
    pm = PlanManager()
    p1 = TramitePlan(plan_id="p1", tramite="renovacion", country="AR")
    p1.steps = [PlanStep(step_id="s1", description="x", status=__import__("src.agent.orchestrator", fromlist=["StepStatus"]).StepStatus.DONE)]
    p2 = TramitePlan(plan_id="p2", tramite="apostilla", country="AR")
    pm.add_plan("u1", p1)
    pm.add_plan("u1", p2)
    active = pm.get_active_plans("u1")
    assert len(active) == 1
    assert active[0].plan_id == "p2"


def test_remove_plan():
    pm = PlanManager()
    plan = TramitePlan(plan_id="p1", tramite="renovacion", country="AR")
    pm.add_plan("u1", plan)
    assert pm.remove_plan("u1", "p1") is True
    assert pm.get_plan("u1", "p1") is None
    assert pm.remove_plan("u1", "p1") is False


def test_get_plans_empty_for_unknown_user():
    pm = PlanManager()
    assert pm.get_plans("unknown") == []