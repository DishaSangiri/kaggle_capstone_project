from typing import Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase

class ButterflyAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Butterfly",
            instruction=(
                "You are the Butterfly Agent. Your task is to calculate chaotic 'butterfly effects' "
                "where micro-changes in habit metrics cascade into unexpected shifts in ecosystem health."
            )
        )

    def process(self, db: Session, cycle_id: str, current_metrics: Dict[str, float], patterns: Dict[str, Any]) -> Dict[str, Any]:
        cascade_threat = "none"
        impact_level = "low"

        if current_metrics.get("wellness", 0.5) < 0.4 and patterns.get("burnout_risk", False):
            cascade_threat = "Wellness drain triggers a cognitive fog event, decreasing Atmospheric Clarity by 30%."
            impact_level = "high"

        effects = {
            "cascade_threat": cascade_threat,
            "system_entropy": 0.2 if impact_level == "low" else 0.7,
            "impact_level": impact_level
        }

        self.adk_agent.run(f"Calculate butterfly cascades: metrics={current_metrics}, patterns={patterns}")

        rationale = f"Completed chaos check. Ecosystem cascade risk is {impact_level.upper()}. Threat: {cascade_threat}"
        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="SIMULATED_CHAOS_CASCADES",
            status="SUCCESS",
            rationale=rationale,
            impact=effects
        )

        return effects
