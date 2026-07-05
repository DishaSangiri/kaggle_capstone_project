from typing import Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase

class FinanceGovernorAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Finance Governor",
            instruction=(
                "You are the Finance Governor. You manage the industrial hubs and crystal energy columns. "
                "The health of these crystal columns depends on user spending limits, budget scores, and savings habits."
            )
        )

    def process(self, db: Session, cycle_id: str, current_metrics: Dict[str, float]) -> float:
        finance = current_metrics.get("finance", 0.5)
        finance_health = max(min(finance, 1.0), 0.0)

        self.adk_agent.run(f"Evaluate finance biome: finance={finance}")

        rationale = f"Crystal columns and asset structures analyzed. Financial budget score of {finance:.2f} maps to finance biome health of {finance_health:.2f}."
        impact = {"finance_health": finance_health}

        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="EVALUATED_FINANCE_BIOME",
            status="SUCCESS",
            rationale=rationale,
            impact=impact
        )

        return finance_health
