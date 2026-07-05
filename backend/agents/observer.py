from typing import List, Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase
from app.models import UserHabit

class ObserverAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Observer",
            instruction=(
                "You are the Observer Agent. Your goal is to gather raw, unstructured habit data "
                "from user inputs and consolidate them into clean, structured habit category metrics."
            )
        )

    def process(self, db: Session, cycle_id: str, habits: List[UserHabit]) -> Dict[str, Any]:
        """Consolidates list of habits into category-wise aggregates (0.0 to 1.0 scales)."""
        categories = ["focus", "wellness", "finance", "health"]
        scores = {cat: 0.5 for cat in categories}
        counts = {cat: 0 for cat in categories}

        for habit in habits:
            if habit.category in scores:
                scores[habit.category] += habit.value
                counts[habit.category] += 1

        for cat in categories:
            if counts[cat] > 0:
                scores[cat] = min(max(scores[cat] / (counts[cat] * 10.0), 0.0), 1.0)
            else:
                scores[cat] = 0.5

        # Run ADK agent block
        self.adk_agent.run(f"Aggregate habits: {str(scores)}")

        rationale = f"Observed {len(habits)} user actions. Consolidated score: Focus={scores['focus']:.2f}, Wellness={scores['wellness']:.2f}, Finance={scores['finance']:.2f}."
        impact = {"metrics": scores}

        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="AGGREGATED_HABITS",
            status="SUCCESS",
            rationale=rationale,
            impact=impact
        )

        return scores
