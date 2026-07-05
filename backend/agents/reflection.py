from sqlmodel import Session
from agents.base import RealityAgentBase

class ReflectionAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Reflection",
            instruction=(
                "You are the Reflection Agent. You craft philosophical and mindful insights based on "
                "the overall balance of the planet, prompting the user with existential or psychological self-reflection."
            )
        )

    def process(self, db: Session, cycle_id: str, equilibrium: float) -> str:
        reflection = ""
        if equilibrium >= 0.7:
            reflection = (
                "Your RealityVerse is vibrant and aligned. When focus and self-care flow in unison, "
                "the world requires very little effort to remain in balance. What was the catalyst for today's ease?"
            )
        elif equilibrium <= 0.4:
            reflection = (
                "The winds are cold and the oceans are heavy. You are expending energy on work "
                "but neglecting the soil beneath you. What boundary can you draw today to reclaim your space?"
            )
        else:
            reflection = (
                "The world sits in quiet expectation. Neither decaying nor blooming, it waits for a conscious choice. "
                "Where will you plant your focus next?"
            )

        self.adk_agent.run(f"Formulate reflection: equilibrium={equilibrium}")

        impact = {"reflection": reflection}
        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="GENERATED_PHILOSOPHICAL_REFLECTION",
            status="SUCCESS",
            rationale=f"Constructed equilibrium prompt matching {equilibrium:.2f} balance rating.",
            impact=impact
        )

        return reflection
