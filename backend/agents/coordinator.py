import uuid
import json
from typing import List, Any
from sqlmodel import Session
from app.models import PlanetState, UserHabit
from agents.base import RealityAgentBase

class RealityCoordinatorAgent(RealityAgentBase):
    def __init__(self, registry: Any = None):
        super().__init__(
            name="Reality Coordinator",
            instruction=(
                "You are the Reality Coordinator. Your role is to orchestrate all specialized "
                "agents in the RealityVerse system, aggregate their analytics, and commit "
                "the newly generated state to the 3D world configuration."
            )
        )
        # Registry dependency injected via constructor or cycle execution method
        self.registry = registry

    def run_cycle(self, db: Session, raw_habits: List[UserHabit], registry: Any = None) -> PlanetState:
        """
        Runs the full 10-agent orchestration sequence.
        Resolves sub-agents using Dependency Injection from the registry context.
        Returns the finalized 3D PlanetState model.
        """
        active_registry = registry or self.registry
        if not active_registry:
            raise ValueError("An AgentRegistry dependency must be provided to run the coordination cycle.")

        cycle_id = str(uuid.uuid4())
        
        # Resolve specialist agent instances from the DI registry container
        observer = active_registry.get_agent("Observer")
        pattern = active_registry.get_agent("Pattern")
        butterfly = active_registry.get_agent("Butterfly")
        forest_gov = active_registry.get_agent("Forest Governor")
        ocean_gov = active_registry.get_agent("Ocean Governor")
        finance_gov = active_registry.get_agent("Finance Governor")
        focus_gov = active_registry.get_agent("Focus Governor")
        future_sim = active_registry.get_agent("Future Simulation")
        reflection = active_registry.get_agent("Reflection")
        
        # 1. Observer
        metrics = observer.process(db, cycle_id, raw_habits)
        
        # 2. Pattern Detector
        patterns = pattern.process(db, cycle_id, metrics)
        
        # 3. Chaos Butterfly Simulation
        butterfly_effect = butterfly.process(db, cycle_id, metrics, patterns)
        
        # 4. Biome Governor evaluations
        forest_val = forest_gov.process(db, cycle_id, metrics)
        ocean_val = ocean_gov.process(db, cycle_id, metrics)
        finance_val = finance_gov.process(db, cycle_id, metrics)
        focus_val = focus_gov.process(db, cycle_id, metrics)
        
        # 5. Core Equilibrium computation
        equilibrium = (forest_val + ocean_val + finance_val + focus_val) / 4.0
        
        # 6. Future forecasting (30 Days out)
        projections = future_sim.process(
            db, 
            cycle_id, 
            {"forest": forest_val, "ocean": ocean_val, "finance": finance_val, "focus": focus_val},
            butterfly_effect.get("system_entropy", 0.5)
        )
        
        # 7. Philosophical Reflection prompt
        reflection_text = reflection.process(db, cycle_id, equilibrium)
        
        # Compile simulation metadata
        simulation_data = {
            "projection_30d": projections,
            "chaos_entropy": butterfly_effect.get("system_entropy", 0.5),
            "reflection": reflection_text,
            "patterns": patterns
        }
        
        # Reconcile outputs into a single unified PlanetState
        planet_state = PlanetState(
            forest_health=forest_val,
            ocean_health=ocean_val,
            finance_health=finance_val,
            focus_health=focus_val,
            overall_equilibrium=equilibrium,
            agent_version="v2.0.0-ADK",
            simulation_projection=json.dumps(simulation_data)
        )
        
        db.add(planet_state)
        db.commit()
        db.refresh(planet_state)
        
        # Log self completion
        self.log_execution(
            db=db,
            cycle_id=cycle_id,
            action="COORDINATED_CYCLE",
            status="SUCCESS",
            rationale=f"Orchestrated 9 sub-agents via DI Registry lookup. Equilibrium established at {equilibrium:.2f}.",
            impact={
                "planet_state_id": planet_state.id,
                "equilibrium": equilibrium
            }
        )
        
        return planet_state
