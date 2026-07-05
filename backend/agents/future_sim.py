from typing import Dict, Any
from sqlmodel import Session
from agents.base import RealityAgentBase

class FutureSimulationAgent(RealityAgentBase):
    def __init__(self):
        super().__init__(
            name="Future Simulation",
            instruction=(
                "You are the Future Simulation Agent. You analyze the current state of all biomes "
                "and predict how the planet will evolve over a 30-day projection cycle, based on current "
                "behavioral streaks and entropy levels."
            )
        )

    def process(self, db: Session, cycle_id: str, current_states: Dict[str, float], entropy: float) -> Dict[str, Any]:
        growth_factor = 0.05 if entropy < 0.4 else -0.1
        
        projections = {}
        for biome, health in current_states.items():
            projected = max(min(health + growth_factor, 1.0), 0.0)
            projections[biome] = round(projected, 2)

        self.adk_agent.run(f"Project 30-day outlook: states={current_states}, entropy={entropy}")

        rationale = f"Forecast run complete. Projecting a 30-day { 'decay' if growth_factor < 0 else 'equilibrium' } with an average biome adjustment of {growth_factor*100:+.0f}%."
        impact = {"projected_30d_biomes": projections}

        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="PROJECTED_FUTURE_STATES",
            status="SUCCESS",
            rationale=rationale,
            impact=impact
        )

        return projections
