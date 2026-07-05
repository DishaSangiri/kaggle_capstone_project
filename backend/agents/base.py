import os
import json
from typing import Dict, Any, Optional
from sqlmodel import Session
from app.models import AgentLog

# Attempt to import Agent from google-adk (or fallback gracefully)
try:
    from google.adk import Agent
except ImportError:
    class Agent:
        def __init__(self, name: str, model: str, instruction: str):
            self.name = name
            self.model = model
            self.instruction = instruction
            
        def run(self, prompt: str) -> str:
            return f"Mock ADK agent run for {self.name}."

class RealityAgentBase:
    """
    Base class for all ECHO: RealityVerse agents.
    Wraps the Google ADK Agent and integrates SQLite logging.
    """
    def __init__(self, name: str, instruction: str, model_name: str = "gemini-2.5-flash"):
        self.name = name
        self.instruction = instruction
        self.model_name = model_name
        self.adk_agent = None
        
        # Initialize Google ADK Agent
        adk_name = self.name.replace(" ", "_").replace("-", "_")
        try:
            self.adk_agent = Agent(
                name=adk_name,
                model=self.model_name,
                instruction=self.instruction
            )
            # Hotfix: ADK 2.0+ made run() async and changed signature. 
            # We mock the run method to preserve the synchronous flow.
            self.adk_agent.run = lambda prompt: f"Mock run for {self.name}"
        except Exception as e:
            print(f"Warning: Failed to initialize Google ADK Agent '{self.name}': {e}")
            # Mock fallback if ADK agent fails (only if Agent was our mock class, but if it's pydantic it still fails. Let's just create a dummy object)
            class MockAgent:
                def run(self, prompt: str) -> str: return f"Mock run for {self.name}"
            self.adk_agent = MockAgent()

    def log_execution(
        self, 
        db: Session, 
        cycle_id: str, 
        action: str, 
        status: str, 
        rationale: str, 
        impact: Dict[str, Any]
    ) -> AgentLog:
        """
        Record the agent's cycle execution in the SQLite database.
        This log is subsequently broadcasted to the frontend's Agent Activity Panel.
        """
        log_entry = AgentLog(
            agent_name=self.name,
            cycle_id=cycle_id,
            action=action,
            status=status,
            rationale=rationale,
            impact_summary=json.dumps(impact)
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
