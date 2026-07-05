from typing import Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase

class PatternAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Pattern",
            instruction=(
                "You are the Pattern Agent. Your task is to detect recurring patterns and behavioral "
                "loops over time, flagging streaks, burnout risks, or optimization windows."
            )
        )

    def process(self, db: Session, cycle_id: str, current_metrics: Dict[str, float]) -> Dict[str, Any]:
        streaks = []
        burnout_risk = False

        if current_metrics.get("focus", 0.5) > 0.8:
            streaks.append("Productivity streak detected")
            if current_metrics.get("wellness", 0.5) < 0.3:
                burnout_risk = True

        patterns = {
            "streaks": streaks,
            "burnout_risk": burnout_risk,
            "habit_consistency": "stabilizing"
        }

        self.adk_agent.run(f"Identify behavior pattern from: {current_metrics}")

        rationale = f"Analyzed trend metrics. Streaks: {streaks or 'none'}. Burnout risk flagged: {burnout_risk}."
        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="DETECTED_PATTERNS",
            status="SUCCESS",
            rationale=rationale,
            impact=patterns
        )

        return patterns
