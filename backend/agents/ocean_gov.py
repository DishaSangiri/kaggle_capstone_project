from typing import Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase

class OceanGovernorAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Ocean Governor",
            instruction=(
                "You are the Ocean Governor. You manage the oceans, lakes, and cloud covers of the planet. "
                "The health of the ocean responds to mental clarity, hydration, and clean nutrition habits."
            )
        )

    def process(self, db: Session, cycle_id: str, current_metrics: Dict[str, float]) -> float:
        wellness = current_metrics.get("wellness", 0.5)
        ocean_health = max(min(wellness * 1.1, 1.0), 0.1)

        self.adk_agent.run(f"Evaluate ocean biome: wellness={wellness}")

        rationale = f"Ocean currents and water bodies analyzed. Wellness hydration score of {wellness:.2f} results in ocean health level of {ocean_health:.2f}."
        impact = {"ocean_health": ocean_health}

        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="EVALUATED_OCEAN_BIOME",
            status="SUCCESS",
            rationale=rationale,
            impact=impact
        )

        return ocean_health
