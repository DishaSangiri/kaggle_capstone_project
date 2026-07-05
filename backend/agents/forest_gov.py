from typing import Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase

class ForestGovernorAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Forest Governor",
            instruction=(
                "You are the Forest Governor. You manage the forest biomes of the 3D RealityVerse planet. "
                "The health of the forest responds to user wellness, physical health, and activity habits."
            )
        )

    def process(self, db: Session, cycle_id: str, current_metrics: Dict[str, float]) -> float:
        wellness = current_metrics.get("wellness", 0.5)
        health = current_metrics.get("health", 0.5)

        forest_health = (wellness + health) / 2.0

        self.adk_agent.run(f"Evaluate forest biome: wellness={wellness}, health={health}")

        rationale = f"Forest flora evaluated. Wellness input ({wellness:.2f}) and Health input ({health:.2f}) yield a biome health index of {forest_health:.2f}."
        impact = {"forest_health": forest_health}

        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="EVALUATED_FOREST_BIOME",
            status="SUCCESS",
            rationale=rationale,
            impact=impact
        )

        return forest_health
