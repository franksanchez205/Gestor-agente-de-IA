"""Orquestador de acciones del agente.

Planifica los pasos de un trámite, coordina la capa de acción (invisible
para el cliente) y pide confirmación humana en puntos críticos.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Awaitable


class StepStatus(str, Enum):
    PENDING = "pending"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class PlanStep:
    step_id: str
    description: str
    action: Callable[[], Awaitable[dict]] | None = None
    requires_confirmation: bool = False
    status: StepStatus = StepStatus.PENDING
    result: dict | None = None


@dataclass
class TramitePlan:
    plan_id: str
    tramite: str
    country: str
    steps: list[PlanStep] = field(default_factory=list)

    @property
    def next_pending(self) -> PlanStep | None:
        for s in self.steps:
            if s.status == StepStatus.PENDING:
                return s
        return None

    @property
    def is_complete(self) -> bool:
        return all(s.status == StepStatus.DONE for s in self.steps)


class Orchestrator:
    """Coordina la ejecución de un plan de trámite."""

    def __init__(self, confirm_callback: Callable[[str], Awaitable[bool]]):
        self.confirm_callback = confirm_callback

    async def run(self, plan: TramitePlan) -> TramitePlan:
        for step in plan.steps:
            if step.status != StepStatus.PENDING:
                continue
            if step.requires_confirmation:
                step.status = StepStatus.AWAITING_CONFIRMATION
                ok = await self.confirm_callback(step.description)
                if not ok:
                    step.status = StepStatus.FAILED
                    break
            step.status = StepStatus.RUNNING
            try:
                if step.action is not None:
                    step.result = await step.action()
                step.status = StepStatus.DONE
            except Exception as exc:  # noqa: BLE001
                step.status = StepStatus.FAILED
                step.result = {"error": str(exc)}
                break
        return plan