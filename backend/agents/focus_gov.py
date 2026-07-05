from typing import Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase

class FocusGovernorAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Focus Governor",
            instruction=(
                "You are the Focus Governor. You manage the atmospheric shield and floating citadels. "
                "The health of the citadel shields corresponds directly to user focus levels, deep work hours, "
                "and successful blocking of distractions."
            )
        )

    def process(self, db: Session, cycle_id: str, current_metrics: Dict[str, float]) -> float:
        focus = current_metrics.get("focus", 0.5)
        focus_health = max(min(focus, 1.0), 0.0)

        self.adk_agent.run(f"Evaluate focus biome: focus={focus}")

        rationale = f"Citadel focus fields evaluated. Focus habits of {focus:.2f} yield Citadel Shield efficiency at {focus_health:.2f}."
        impact = {"focus_health": focus_health}

        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="EVALUATED_FOCUS_BIOME",
            status="SUCCESS",
            rationale=rationale,
            impact=impact
        )

        return focus_health
