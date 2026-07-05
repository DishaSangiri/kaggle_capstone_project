from typing import Dict, Any
from agents.base import RealityAgentBase
from agents.observer import ObserverAgent
from agents.pattern import PatternAgent
from agents.butterfly import ButterflyAgent
from agents.forest_gov import ForestGovernorAgent
from agents.ocean_gov import OceanGovernorAgent
from agents.finance_gov import FinanceGovernorAgent
from agents.focus_gov import FocusGovernorAgent
from agents.future_sim import FutureSimulationAgent
from agents.reflection import ReflectionAgent
from agents.coordinator import RealityCoordinatorAgent

class ADKAgentRegistry:
    """
    Registry container for Google ADK agents in ECHO: RealityVerse.
    Enables runtime lookup, modular registration, and dependency injection.
    """
    def __init__(self):
        self._registry: Dict[str, RealityAgentBase] = {}

    def register(self, agent: RealityAgentBase):
        """Register an agent instance by its name."""
        self._registry[agent.name] = agent
        print(f"ADK Registry: Registered agent '{agent.name}' successfully.")

    def get_agent(self, name: str) -> RealityAgentBase:
        """Retrieve an agent instance by name."""
        agent = self._registry.get(name)
        if not agent:
            raise KeyError(f"Agent '{name}' is not registered in the ADK registry.")
        return agent

    def list_agents(self) -> Dict[str, RealityAgentBase]:
        """Return a mapping of all registered agents."""
        return self._registry

# Instantiate the global DI registry
agent_registry = ADKAgentRegistry()

# Register the 10 agents
agent_registry.register(ObserverAgent())
agent_registry.register(PatternAgent())
agent_registry.register(ButterflyAgent())
agent_registry.register(ForestGovernorAgent())
agent_registry.register(OceanGovernorAgent())
agent_registry.register(FinanceGovernorAgent())
agent_registry.register(FocusGovernorAgent())
agent_registry.register(FutureSimulationAgent())
agent_registry.register(ReflectionAgent())

# The Coordinator agent resolves its sub-agents from the registry
agent_registry.register(RealityCoordinatorAgent(registry=agent_registry))
